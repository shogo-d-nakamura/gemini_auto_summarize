from tqdm.contrib import tenumerate
from tqdm import tqdm
import os
import time
import google.generativeai as genai
import argparse
from pypdf import PdfReader

parser = argparse.ArgumentParser()
parser.add_argument('--input', '-i', type=str, help='入力ファイルのパス')
parser.add_argument('--batch', '-b', type=str, help='複数ファイルをバッチ処理する場合のディレクトリ')
parser.add_argument('--pro', '-p', action='store_true', help='Gemini-1.5-Proを使用する場合に指定')
args = parser.parse_args()
input = args.input
if args.pro:
    print("Gemini-1.5-Proを使用します。")
else:
    print("Gemini-1.5-Flashを使用します。")
    
filepath = "path/to/pdf"

# set api key
with open('gemini_api', 'r') as f:
    GOOGLE_API_KEY = f.read().rstrip()
genai.configure(api_key=GOOGLE_API_KEY)

# set prompts
prompts = [f"これから、英語論文のテキストを入力します。これを読み込み、この論文の内容について、日本語で詳しく説明してください。",
           "この論文のIntroductionの内容について、詳しく説明してください。",
           "引用されている論文の中で、重要なものをいくつか取り上げて、詳しく説明してください。",
           "この論文の中で利用されているデータセットについて、詳しく説明してください。",
           "この論文で行われた全ての実験について、その結果を詳しく説明してください。",
           "それぞれについて、さらに詳しく説明してください。",
           "その実験の結果を受けて、論文の中で考察されていることについて詳しく説明してください。",
           "この論文で提案されている手法について、詳しく説明してください。",
           "それぞれの項目について、さらに詳しく説明してください。",
           "それぞれの実験について、具体的な手続きを説明してください。",
           "それぞれの項目について、さらに詳しく説明してください。",
           "この論文のConclusionについて、詳しく説明してください。",
           "この論文の関連研究について、詳しく説明してください。",
           "この論文の新規性がどこか、詳しく説明してください。",
           "提案手法が、従来研究よりも優れている点について、詳しく説明してください。",
           "提案手法の課題について、詳しく説明してください。" 
           ]

def read_pdf(filepath, input):
    reader = PdfReader(filepath + input)
    num_pages = len(reader.pages)
    pdf_input = []
    for p in range(num_pages):
        text = reader.pages[p].extract_text()
        pdf_input.append(text)
    pdf_input = ' '.join(pdf_input)
    return pdf_input

def gen_chat(prompts, pdf_input, gen_config, safety_settings, flash=False):
  if flash:
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
  else:
    model = genai.GenerativeModel('gemini-1.5-pro-latest')
  flag = False
  chat = model.start_chat(history=[])
  for i, prompt in tenumerate(prompts):
    if i == 0:
        prompt = f"{prompt} \n {pdf_input}."
        response_text, lim_flag = gen_text(chat, prompt, gen_config, safety_settings)
        if flash:
          time.sleep(1)
        else:
          time.sleep(30)
    else:
        response_text, lim_flag = gen_text(chat, prompt, gen_config, safety_settings)
        if flash:
          time.sleep(1)
        else:
          time.sleep(30)
    if lim_flag:
      print("request limit: changing model to gemini-flash...")
      break
  return chat, lim_flag

def gen_text(chat, prompt, gen_config, safety_settings, flag=False):
    try:
       response = chat.send_message(content=prompt, generation_config=gen_config,safety_settings=safety_settings)
       return response.text, flag
    except Exception as e:
        print(f"ERROR: {e}")
        flag = True
        if 'response' in locals():
            print(f"\n\nPrompt Feedback: {response.prompt_feedback}\n\nResponse Dict:\n{response.__dict__}")
        return None, flag

def remove_extension(filename):
    base_name, _ = os.path.splitext(filename)
    return base_name


def make_md(filepath, input):
    # read pdf file
    pdf_input = read_pdf(filepath, input)
    safety_settings=[
        { "category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE" },
        { "category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE" },
        { "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE" },
        { "category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
    ]
    gen_config = {"temperature": 0.8}
    if args.pro:
        chat, lim_flag = gen_chat(prompts, pdf_input, gen_config, safety_settings, flash=False)
        # proでrequest limitかサーバービジーなどのエラーが発生した場合、flashに切り替える
        if lim_flag:
            chat, _ = gen_chat(prompts, pdf_input, gen_config, safety_settings, flash=True)
    else:
        chat, _ = gen_chat(prompts, pdf_input, gen_config, safety_settings, flash=True)

    output = []
    for i, message in enumerate(chat.history):
        role = "You" if i % 2 == 0 else "Gemini"
        if i == 0:
            output.append(f"# {role}:\n {prompts[0]} (省略)") # PDFの内容は長いので省略
        else:
            output.append(f"# {role}:\n {message.parts[0].text}")

    filename = remove_extension(input) + ".md"
    with open(filepath + filename, "w") as file:
        file.write("\n\n".join(output))

def main():
    if args.input:
        make_md(filepath, input)
    elif args.batch:
        files = os.listdir(filepath + args.batch)
        print(f"Processing {len(files)} files...")
        for file in tqdm(files):
            if file.endswith(".pdf"):
                make_md(filepath + args.batch + '/', file)
    else:
        print("Please specify input file or batch directory.")

if __name__ == '__main__':
    main()
