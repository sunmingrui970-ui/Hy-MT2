import argparse
import json
import utils

def main():
    parser = argparse.ArgumentParser()
    
    parser.add_argument('input_file', help='输入文件路径')
    parser.add_argument('--output_file', help='输出文件路径')

    args = parser.parse_args()
    print(f"处理文件: {args.input_file}")
    if args.output_file:
        print(f"输出到: {args.output_file}")
        fw = open(args.output_file, "w")

    with open(args.input_file) as f:
        for line in f:
            l = json.loads(line)
            messages = l["messages"]
            extra = l["extra"]
            xcomet_score_list = l["xcomet_score_list"]
            if xcomet_score_list[0] > xcomet_score_list[1]:
                answer = l["correct_res"][0]
                messages.append({"role": "assistant", "content": [{"type": "Thinking", "value": ""}, {"type": "Summary", "value": answer}]})
                to_save = {"system_prompt": "", "messages": messages, "loss_mask": [0, 1], "topic": "机器翻译", "is_business": 0, "task": "zhiyan日志", "language": "", "answer": answer, "RL_ONLY": 1}
                to_save["prompt"] = l["prompt"]
                to_save["origin_language"] = extra["src_lang"]
                to_save["target_language"] = extra["target_lang"]
                to_save["origin_text"] = l["origin_text"]
                fw.write(json.dumps(to_save, ensure_ascii=False) + "\n")

if __name__ == '__main__':
    main()