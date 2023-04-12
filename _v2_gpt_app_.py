import openai
import os
import json
import glob

# APIキーの設定
openai.organization = "Your organization key"
openai.api_key = "Your API key"

# GPTモデルを使った質問と回答の処理
def ask_gpt(prompt, conversation_history):
    # ユーザーの質問を会話履歴に追加
    conversation_history.append({"role": "user", "content": prompt})
    
    # GPTに質問を投げ、回答を受け取る
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=conversation_history,
    )

    # GPTからの回答を取得し、会話履歴に追加
    answer = response['choices'][0]['message']['content']
    conversation_history.append({"role": "assistant", "content": answer})
    return answer

# 会話履歴をファイルに保存する関数
def save_conversation_to_file(conversation_history, file_path):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(conversation_history, f, ensure_ascii=False, indent=4)

# ファイルから会話履歴を読み込む関数
def load_conversation_from_file(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            conversation_history = json.load(f)
    else:
        conversation_history = [{"role": "system", "content": "You are a helpful assistant."}]

    return conversation_history

# 会話履歴ファイルのリストから選択する機能を実装
def select_conversation_file():
    files = glob.glob("*.json")
    
    print("利用可能な会話履歴ファイル:")
    for idx, file in enumerate(files, start=1):
        print(f"{idx}. {file}")

    print(f"{len(files) + 1}. 新規の会話履歴ファイルを作成")

    selected_idx = int(input("会話履歴ファイルを選択してください（番号を入力）: "))

    if selected_idx == len(files) + 1:
        new_file_name = input("新規の会話履歴ファイル名を入力してください（.json拡張子は不要）: ")
        if not new_file_name.endswith('.json'):
            new_file_name += '.json'
        return new_file_name
    else:
        return files[selected_idx - 1]

# メインのアプリ
def main():
    print("GPTアプリへようこそ！　質問を入力してください。")
    print("終了するには 'q' と入力してください。")

    # 会話履歴ファイルを選択
    file_path = select_conversation_file()

    # 会話履歴をファイルから読み込む
    conversation_history = load_conversation_from_file(file_path)

    while True:
        user_input = input("\n質問: ")
        if user_input.lower() == "q":
            # 終了時に会話履歴をファイルに保存
            save_conversation_to_file(conversation_history, file_path)
            break

        # GPTに質問を投げ、回答を受け取る
        response = ask_gpt(user_input, conversation_history)
        print(f"GPTの回答: {response}")

if __name__ == "__main__":
    main()