from flask import Flask, request, jsonify, Response, stream_with_context
from dotenv import load_dotenv
from datetime import datetime
from system_prompt_modality_B import get_system_prompt_modality_B
from system_prompt_modality_C import get_system_prompt_modality_C
import os

os.environ['OPENBLAS_NUM_THREADS'] = "1"
import pandas as pd
import __main__

__main__.pd = pd
from flask_cors import CORS

# Load environment variables from .env file
load_dotenv()

MyApp = Flask(__name__)
CORS(MyApp)
# CORS(MyApp,resources={r"/*": {"origins": "*"}})
# CORS(MyApp, origins=["http://py-rates.fr",
#                       "https://py-rates.fr",
#                       "http://py-rates.org",
#                       "https://py-rates.org"])
application = MyApp

# ---- Environment variables ----
llm_api = os.getenv('LLM_API')
llm_api_key = os.getenv('LLM_API_KEY')
llm_url = os.getenv('LLM_URL')
llm_model = os.getenv('LLM_MODEL')

# ---- Init client depending on API ----
if llm_api == "mistral":
    from mistralai import Mistral

    client = Mistral(api_key=llm_api_key)  # no need base_url here
else:
    from openai import OpenAI

    client = OpenAI(
        base_url=llm_url,
        api_key=llm_api_key,
    )

# ---- Common LLM parameters ----
llm_params = {
    # temperature : Controls the randomness of the responses [0.0,2.0] / def = 1.0
    "temperature": 0.3,
    # 0.3 -> Lower temperature reduces randomness. This ensures factual, consistent, and clear responses.
    # max_tokens : Maximum length of the generated response [0,model max] / def = no def
    "max_tokens": 500,  # 500 -> Allows for reasonably detailed explanations without being too verbose.
    # top_p : Nucleus sampling to filter unlikely tokens [0.0,1.0] / def = 1.0
    "top_p": 0.9,  # 0.9 -> Helps avoid unlikely creative words while keeping some diversity
    # presence_penalty : Discourages repeating earlier tokens [-2.0,2.0] / def = 0.0
    "presence_penalty": 0, # 0 -> Default value
    # frequency_penalty: Reduces exact repetitions [-2.0,2.0] / def = 0.0
    "frequency_penalty": 0, # 0-> Default value
}

# ---- Accepted input values ----
accepted_levels = [1, 2, 3, 4, 5, 6, 7, 8]
accepted_languages = ["EN", "FR"]
accepted_modalities = [1, 2]


@MyApp.route("/llm-inference-stream", methods=["POST"])
def get_llm_inference_stream():
    # print("----------------------------------")
    # print("Start POST llm_inference_stream")
    # print("----------------------------------")
    # print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}][INFO] Used model : {llm_model} with {llm_api} API")
    # print(f"[INFO] Used model : {llm_model} with {llm_api} API")
    # print(f"[INFO] Model parameters:")
    # print(f"  - temperature: {llm_params['temperature']}")
    # print(f"  - max_tokens: {llm_params['max_tokens']}")
    # print(f"  - top_p: {llm_params['top_p']}")
    # print(f"  - presence_penalty: {llm_params['presence_penalty']}")
    # print(f"  - frequency_penalty: {llm_params['frequency_penalty']}")
    try:
        # Extract request parameters
        level_id = request.args.get('level_id', type=int)
        language = request.args.get('language', type=str)
        modality = request.args.get('modality', type=int)
        content = request.get_json()
        user_messages = content.get('messages', [])

        # Input validation
        if not level_id or level_id not in accepted_levels:
            return jsonify({"error": "Invalid level_id"}), 400
        if not language or language not in accepted_languages:
            return jsonify({"error": "Invalid language"}), 400
        if not modality or modality not in accepted_modalities:
            return jsonify({"error": "Invalid modality"}), 400
        if not user_messages:
            return jsonify({"error": "Messages array is empty"}), 400

        # print("Modality: "+str(modality))

        # Build prompt
        system_message = {}
        if modality == 1 :
            system_message = get_system_prompt_modality_B(level_id, language)
        elif modality == 2 :
            system_message = get_system_prompt_modality_C(level_id, language)
    
        full_messages = [system_message] + user_messages

        # print(full_messages)

        def generate():
            try:
                # print("LLM API Calling")
                # --- Call Mistral API ---
                if llm_api == "mistral":
                    response = client.chat.stream(
                        model=llm_model,
                        messages=full_messages,
                        **llm_params  # Inject common params
                    )
                    has_content = False
                    for chunk in response:
                        if chunk.data.choices and chunk.data.choices[0].delta:
                            content = chunk.data.choices[0].delta.content
                            if content:  # Only send non-empty chunks
                                has_content = True
                                # Escape new lines du to SSE format: "data: [content]\n\n" ou "error: [error message]\n\n"
                                escaped_content = content.replace('\n', '\\n')
                                # Stream the chunk
                                yield f"data: {escaped_content}\n\n"

                    if not has_content:
                        error_message = "POST llm_inference_stream : empty response from Mistral"
                        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [ERROR] {error_message}")
                        # print("[ERROR]" + error_message)
                        yield f"error: {error_message}\n\n"
                # --- Call OpenAI API (or compatible) ---
                else:
                    response = client.chat.completions.create(
                        model=llm_model,
                        messages=full_messages,
                        stream=True,
                        **llm_params  # Inject common params
                    )
                    has_content = False  # Flag to check if any content was received

                    for chunk in response:
                        if chunk.choices and chunk.choices[0].delta:
                            content = chunk.choices[0].delta.content
                            if content:  # Only send non-empty chunks
                                has_content = True
                                # Escape new lines du to SSE format: "data: [content]\n\n" ou "error: [error message]\n\n"
                                escaped_content = content.replace('\n', '\\n')
                                # Stream the chunk
                                yield f"data: {escaped_content}\n\n"

                    # If no content was generated by the model
                    if not has_content:
                        error_message = "POST llm_inference_stream : empty response from LLM"
                        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [ERROR] {error_message}")
                        # print("[ERROR]" + error_message)
                        yield f"error: {error_message}\n\n"

            except Exception as e:
                error_message = "POST llm_inference_stream : " + str(e)
                print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [ERROR] {error_message}")
                # print("[ERROR]" + error_message)
                yield f"error: {error_message}\n\n"

        # print("----------------------------------")
        # print("End POST llm_inference_stream")
        # print("----------------------------------")
        # Use EventStream to prevent buffering
        return Response(stream_with_context(generate()), content_type="text/event-stream")

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500