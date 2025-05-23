import re

def detect_lang_mix_zh2other(input_str):
    lang_name_map = {
        "ko": "韩语",
        "ru": "俄语",
        "vi": "越南语",
        "th": "泰语",
        "de": "德语",
        "ar": "阿拉伯语",
        "fr": "法语",
        "pt": "葡萄牙语",
        "tr": "土耳其语",
        "ms": "马来语",
        "es": "西班牙语",
        "it": "意大利语",
        "id": "印尼语",
        "en": "英语"
    }
    chinese_pattern = re.compile(r'[\u4e00-\u9fa5]+')
    chinese_phrases = chinese_pattern.findall(input_str)
    is_mix = False
    mix_len = 0
    mix_str = ""
    if len(chinese_phrases) > 0:
        is_mix = True
        mix_str = "".join(chinese_phrases)
        mix_len = len(mix_str)
    return is_mix, mix_len, mix_str

def parse_ds_r1_output():
    pass

def gen_t1_sft_messages_single_turn(question, think, answer):
    messages = [{"role": "user", "content": question}, 
                {"role": "assistant", "content": [{"type": "Thinking", "value": think}, {"type": "Summary", "value": answer}]}]
    return messages

def get_qa_from_t1_sft_messages(messages):
    q = messages[0]["content"]
    a = ""
    think = ""
    if "value" in messages[1]["content"][-1]:
        a = messages[1]["content"][-1]["value"]
    if "value" in messages[1]["content"][-2]:
        think = messages[1]["content"][-2]["value"]
    return q, think, a