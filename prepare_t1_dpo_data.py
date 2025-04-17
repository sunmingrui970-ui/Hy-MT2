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

    data = {}
    count = 0
    bad_count = 0
    with open(args.input_file) as f:
        for line in f:
            l = json.loads(line)
            #score = l["XCOMET-XXL_withref_score"]
            #input = l["origin_text"]
            #if input not in data:
            #    data[input] = []
            #data[input].append({"l":l, "score": score})
            messages = l["messages"]
            if len(messages) == 2:
                question, answer = utils.get_qa_from_t1_sft_messages(l["messages"])
                if len(question) < 20:
                    if (len(answer) < 20 and "解释" not in question) or (len(answer) > 20 and "解释" in question):
                        #to_save = {"question": question, "answer": answer}
                        #fw.write(json.dumps(to_save, ensure_ascii=False) + "\n")
                        continue
            fw.write(line)
            
        '''
        for input in data:
            max_score = 0
            min_score = 1
            avg_score = 0
            max_answer = ""
            min_answer = ""
            for item in data[input]:
                score = item["score"]
                if score < min_score:
                    min_score = score
                    min_answer = item["l"]["answer_only"]
                elif score > max_score:
                    max_score = score
                    max_answer = item["l"]["answer_only"]
                avg_score += score
            avg_score /= len(data[input])
            if min_score < 0.6 and max_score > 0.7:
                count += 1
                to_save = {"input": input, "better": max_answer, "worse": min_answer}
                fw.write(json.dumps(to_save, ensure_ascii=False) + "\n")
            #print(len(data[input]), avg_score, min_score, max_score)
        '''
    print(count, bad_count)

if __name__ == '__main__':
    main()