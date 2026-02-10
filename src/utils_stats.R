library(car)
library(lme4)
library(emmeans)
library(glmmTMB)
library(pbkrtest)
library(lmerTest)

winsorize_IQR <- function(x, factor = 1.5) {
  
  # Compute quartiles and IQR
  q1  <- quantile(x, 0.25, na.rm = TRUE)
  q3  <- quantile(x, 0.75, na.rm = TRUE)
  iqr <- q3 - q1
  
  # Tukey fences
  lower <- q1 - factor * iqr
  upper <- q3 + factor * iqr
  
  # Prepare output vector
  x_wins <- x
  
  # Count before modifying
  lower_hits <- sum(x < lower, na.rm = TRUE)
  upper_hits <- sum(x > upper, na.rm = TRUE)
  
  # Winsorize
  x_wins[x <  lower] <- lower
  x_wins[x >  upper] <- upper
  
  # Return both vector and counts
  return(list(
    winsorized = x_wins,
    lower_fence = lower,
    upper_fence = upper,
    lower_replacements = lower_hits,
    upper_replacements = upper_hits,
    total_replacements = lower_hits + upper_hits
  ))
}

check_levene_factors =  function(model, model_frame, fixed_factors){
	factors <- unlist(strsplit(fixed_factors, "[*+: ]"))
	factors <- factors[factors != ""]   # remove empty items
	factors <- unique(factors)

	# Run Levene test for each factor
	for (f in factors) {
		cat("\n--- Levene test for factor:", f, "---\n")
		formula_lev <- as.formula(paste0("abs(residuals(model)) ~ as.factor(model_frame[['", f, "']])"))
		print(leveneTest(formula_lev, data = model_frame))
	}
}

check_residuals = function(model){
	print(shapiro.test(residuals(model)))
	qqnorm(residuals(model))
	qqline(residuals(model))
}


checks_lmer_pipeline <- function(df, df_name, dep, fixed_factors, model) {
	# ---- CHECKS ----
	cat("Running checks on:", df_name, "\n")
	cat("Dependent variable:", dep, "\n\n")

	# Assumptions
	dfm <- model.frame(model)
	cat("Levene's Test:\n")
	check_levene_factors(model, dfm, fixed_factors)
	cat("\nShapiro Test:\n")
	check_residuals(model)
}

run_lmer_pipeline <- function(df, df_name, dep, fixed_factors, random_factors) {
  dep_w <- paste0(dep, "_w") # Winsorized variable name
  
  #df[[dep]] = scale(df[[dep]])
  
  # ---- BASE MODEL ----
  #formula <- as.formula(paste0("log(", dep, ")", " ~ ", fixed_factors, " + ", random_factors))
  formula <- as.formula(paste0(dep, " ~ ", fixed_factors, " + ", random_factors))
  model <- lmer(formula, data = df, REML = TRUE)
  print(summary(model))
  
  # ANOVA
  cat("\n- ANOVA for:", deparse(formula), "with", df_name, "\n")
  anova_res = Anova(model, type = 3)
  print(anova_res)
  print(anova(model, type = 3))
  cat("effect size : ", eta2_wald(anova_res[fixed_factors, "Chisq"], nrow(df)))
  
  #emm = emmeans(model, ~ X_group_id)
  emm = emmeans(model, as.formula(paste("~", fixed_factors)))
  print("pariwise comparisons : ")
  print(summary(summary(emm)))
  print(pairs(emm, adjust = "fdr"))
  
  effpairs = eff_size(emm, sigma = sigma(model), edf = df.residual(model))
  print(effpairs)
  
  checks_lmer_pipeline(df = df, df_name=df_name, dep = dep, fixed_factors = fixed_factors, model=model)
  
  # ---- WINSORIZED MODEL ----
  print("WINSORIZED")
  w <- winsorize_IQR(df[[dep]])
  df[[dep_w]] <- as.numeric(w$winsorized)
  
  formula_w <- as.formula(paste0(dep_w, " ~ ", fixed_factors, " + ", random_factors))
  model_w <- lmer(formula_w, data = df, REML = TRUE)
  
  cat("\n- ANOVA for:", deparse(formula_w), "with", df_name, "\n")
  print(Anova(model_w, type = 3))
  
  
  
  # ---- RETURN MODELS ----
  return(list(
    model = model,
    model_w = model_w
  ))
}

eta2_wald <- function(chisq, n) {
  eta2 <- chisq / (chisq + n)
  return(eta2)
}

run_glmm_pipeline <- function(df, df_name, dep, fixed_factors, random_factors) {
  dep_w <- paste0(dep, "_w") # Winsorized variable name
  
  # ---- BASE MODEL ----
  formula <- as.formula(paste0(dep, " ~ ", fixed_factors, " + ", random_factors))
  model <- glmmTMB(formula, data = df, family = nbinom2())
  model <- glmmTMB(formula, data = df, family = poisson)

  
  # ANOVA
  cat("\n- ANOVA for:", deparse(formula), "with", df_name, "\n")
  anova_res = Anova(model, type = 3)
  print(anova_res)
  cat("effect size : ", eta2_wald(anova_res[fixed_factors, "Chisq"], nrow(df)))
  
  #emm = emmeans(model, ~ X_group_id)
  emm = emmeans(model, as.formula(paste("~", fixed_factors)))
  print("pariwise comparisons : ")
  print(summary(summary(emm)))
  print(pairs(emm, adjust = "fdr"))
  
  effpairs = eff_size(emm, sigma = sigma(model), edf = df.residual(model))
  print(effpairs)
  
  # ---- WINSORIZED MODEL ----
  w <- winsorize_IQR(df[[dep]])
  df[[dep_w]] <- as.numeric(w$winsorized)
  
  formula_w <- as.formula(paste0(dep_w, " ~ ", fixed_factors, " + ", random_factors))
  model_w <- glmmTMB(formula_w, data = df, family = nbinom2())
  
  cat("\n- ANOVA for:", deparse(formula_w), "with", df_name, "\n")
  print(Anova(model_w, type = 3))
  
  # ---- RETURN MODELS ----
  return(list(
    model = model,
    model_w = model_w
  ))
}

checks_lm_pipeline <- function(df, df_name, dep, fixed_factors) {
	# ---- CHECKS ----
	cat("Running checks on:", df_name, "\n")
	cat("Dependent variable:", dep, "\n\n")

	# Histogram
	hist(df[[dep]], main = paste("Histogram of", dep))

	# Winsorization check (not storing yet)
	cat("Winsorization stats:\n")
	print(winsorize_IQR(df[[dep]]))
	cat("\n")
	
	# ---- BASE MODEL ----
	formula <- as.formula(paste0(dep, " ~ ", fixed_factors))
	model <- lm(formula, data = df)

	# Assumptions
	dfm <- model.frame(model)
	cat("Levene's Test:\n")
	check_levene_factors(model, dfm, fixed_factors)
	cat("\nShapiro Test:\n")
	check_residuals(model)
}

run_lm_pipeline <- function(df, df_name, dep, fixed_factors) {
  dep_w <- paste0(dep, "_w") # Winsorized variable name
  
  # ---- BASE MODEL ----
  formula <- as.formula(paste0(dep, " ~ ", fixed_factors))
  model <- lm(formula, data = df)
  
  # ANOVA
  cat("\n- ANOVA for:", deparse(formula), "with", df_name, "\n")
  print(Anova(model, type = 3))
  
  # ---- WINSORIZED MODEL ----
  w <- winsorize_IQR(df[[dep]])
  df[[dep_w]] <- as.numeric(w$winsorized)
  
  formula_w <- as.formula(paste0(dep_w, " ~ ", fixed_factors))
  model_w <- lm(formula_w, data = df)
  
  cat("\n- ANOVA for:", deparse(formula_w), "with", df_name, "\n")
  print(Anova(model_w, type = 3))
  
  # ---- RETURN MODELS ----
  return(list(
    model = model,
    model_w = model_w
  ))
}




#load data
cleaned_all_data_pyratesLLM2025 <- read.csv("../data/cleaned/cleaned_all_data_pyratesLLM2025.csv",
  fileEncoding = "Windows-1252",
  stringsAsFactors = FALSE)
cleaned_all_data_pyratesLLM2025$X_group_id_BC <- ifelse(cleaned_all_data_pyratesLLM2025$X_group_id == "A", "A", "BC")
cleaned_all_data_pyratesLLM2025[cleaned_all_data_pyratesLLM2025 == "#N/A"] <- NA

cleaned_all_data_pyratesLLM2025$X_learning_gains <- as.numeric(cleaned_all_data_pyratesLLM2025$X_learning_gains)
cleaned_all_data_pyratesLLM2025$X_pre_score <- as.numeric(cleaned_all_data_pyratesLLM2025$X_pre_score)
cleaned_all_data_pyratesLLM2025$X_pre_score_loop <- as.numeric(cleaned_all_data_pyratesLLM2025$X_pre_score_loop)
cleaned_all_data_pyratesLLM2025$X_pre_score_var <- as.numeric(cleaned_all_data_pyratesLLM2025$X_pre_score_var)
cleaned_all_data_pyratesLLM2025$X_pre_score_condi <- as.numeric(cleaned_all_data_pyratesLLM2025$X_pre_score_condi)
cleaned_all_data_pyratesLLM2025$X_post_score <- as.numeric(cleaned_all_data_pyratesLLM2025$X_post_score)
cleaned_all_data_pyratesLLM2025$X_post_score_loop <- as.numeric(cleaned_all_data_pyratesLLM2025$X_post_score_loop)
cleaned_all_data_pyratesLLM2025$X_post_score_var <- as.numeric(cleaned_all_data_pyratesLLM2025$X_post_score_var)
cleaned_all_data_pyratesLLM2025$X_post_score_condi <- as.numeric(cleaned_all_data_pyratesLLM2025$X_post_score_condi)
cleaned_all_data_pyratesLLM2025$X_learning_gains <- as.numeric(cleaned_all_data_pyratesLLM2025$X_learning_gains)
cleaned_all_data_pyratesLLM2025$X_learning_gains_loop <- as.numeric(cleaned_all_data_pyratesLLM2025$X_learning_gains_loop)
cleaned_all_data_pyratesLLM2025$X_learning_gains_var <- as.numeric(cleaned_all_data_pyratesLLM2025$X_learning_gains_var)
cleaned_all_data_pyratesLLM2025$X_learning_gains_condi <- as.numeric(cleaned_all_data_pyratesLLM2025$X_learning_gains_condi)
cleaned_all_data_pyratesLLM2025$X_max_level <- as.numeric(cleaned_all_data_pyratesLLM2025$X_max_level)
cleaned_all_data_pyratesLLM2025$X_max_progression <- as.numeric(cleaned_all_data_pyratesLLM2025$X_max_progression)
cleaned_all_data_pyratesLLM2025$X_progress_index <- as.numeric(cleaned_all_data_pyratesLLM2025$X_progress_index)
cleaned_all_data_pyratesLLM2025$X_teacher_solicitation <- as.numeric(cleaned_all_data_pyratesLLM2025$X_teacher_solicitation)
cleaned_all_data_pyratesLLM2025$X_num_calls <- as.numeric(cleaned_all_data_pyratesLLM2025$X_num_calls)
cleaned_all_data_pyratesLLM2025$X_class_size <- as.numeric(cleaned_all_data_pyratesLLM2025$X_class_size)

cleaned_all_data_pyratesLLM2025$X_gender <- as.factor(cleaned_all_data_pyratesLLM2025$X_gender)
cleaned_all_data_pyratesLLM2025$X_group_id <- as.factor(cleaned_all_data_pyratesLLM2025$X_group_id)
cleaned_all_data_pyratesLLM2025$X_school_id <- as.factor(cleaned_all_data_pyratesLLM2025$X_school_id)
cleaned_all_data_pyratesLLM2025$X_class_id <- as.factor(cleaned_all_data_pyratesLLM2025$X_class_id)

df_all = cleaned_all_data_pyratesLLM2025