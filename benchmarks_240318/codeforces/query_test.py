import os
from openai import OpenAI

# START_DATE = "2023-3-18"
# DATA_DIR = f"./{START_DATE}"
# os.makedirs(DATA_DIR, exist_ok=True)

client = OpenAI(api_key='sk-hs1U5YclOapITjjg01C3A4DdA35045Ff822a59A448E62c49',base_url='https://api.xeduapi.com/v1')


def precision(labels_true, labels_pred):
    true_positive = 0
    predicted_positive = 0
    for true_label, pred_label in zip(labels_true, labels_pred):
        true_positive += sum(1 for true, pred in zip(true_label, pred_label) if true == '1' and pred == '1')
        predicted_positive += sum(1 for pred in pred_label if pred == '1')
    if predicted_positive == 0:
        return 0
    else:
        return true_positive / predicted_positive #预测正确/预测的1个数


def recall(labels_true, labels_pred):
    true_positive = 0
    true_count = 0
    for true_label, pred_label in zip(labels_true, labels_pred):
        true_positive += sum(1 for true, pred in zip(true_label, pred_label) if true == '1' and pred == '1')
        true_count += sum(1 for true in true_label if true == '1')
    if true_count == 0:
        return 0
    else:
        return true_positive / true_count #预测正确/真实的1个数


def f1(labels_true, labels_pred):
    precision_val = precision(labels_true, labels_pred)
    recall_val = recall(labels_true, labels_pred)
    if precision_val + recall_val == 0:
        return 0
    else:
        return 2 * (precision_val * recall_val) / (precision_val + recall_val) #调和平均


def hamming_loss(labels_true, labels_pred):
    num_samples = len(labels_true)
    hamming_loss = sum(sum(1 for true, pred in zip(true_label, pred_label) if true != pred) for true_label, pred_label in zip(labels_true, labels_pred)) / (num_samples * len(labels_true[0]))
    return hamming_loss



def ask(prompt):
    SYSTEM_PROMPT="""
I want you to act as an experienced competitive programmer and problem setter. I will type 
 programmming problem and you should output corresponding tags.The tags and their indexs are as follow:
 
0   brute force

1   data structures

2   implementationd

3   dp

4   greedy

5   math

6   number theory

7   two pointers

8   hashing

9   string suffix structures

10  strings

11  dfs and similar

12  graphs

13  binary search

14  sortings

15  bitmasks

16  shortest paths

17  combinatorics

18  constructive algorithms

19  interactive

20  trees

21  dsu

22  flows

23  games

24  2-sat

25  geometry

26  divide and conquer

27  fft

28  probabilities

29  graph matchings

30  ternary search

31  meet-in-the-middle

32  matrices

33  special problem

34  schedules

35  chinese remainder theorem

36  expression parsing
 
 
 
 I want you to only reply in a string with length of 37.Where the involved tags's corresponding position should be 1,and the rest of them should be 0.For example:1110000000000000000000000000010000001
 
 Here's 3 whole process incidences:
 
 
1.
Input Example:

Hotelier Amugae has a hotel consisting of 10 rooms. The rooms are numbered from 0 to 9 from left to right. The hotel has two entrances — one from the left end, and another from the right end. When a customer arrives at the hotel through the left entrance, they are assigned to an empty room closest to the left entrance. Similarly, when a customer arrives at the hotel through the right entrance, they are assigned to an empty room closest to the right entrance. One day, Amugae lost the room assignment list. Thankfully, Amugae's memory is perfect, and he remembers all of the customers: when a customer arrived, from which entrance, and when they left the hotel. Initially, the hotel was empty. Write a program that recovers the room assignment list from Amugae's memory.

Reasoning:

 To tackle this, we first employ a brute force approach as we need to exhaustively search through all possible room assignment scenarios based on customer arrival information. Next, we utilize data structures such as arrays to organize and manage the room assignment data effectively. Finally, we implement an algorithm to recover the room assignment list by simulating the assignment process, considering the order of customer arrivals and their choice of entrances. This end-to-end process ensures an accurate reconstruction of the room assignment list from the given problem statement.Thus this problem strictly involves and only involves the following tags: brute force, data structures, and implementation,whose tag's number is 0,1,2,so position 0,1,2 should be set to 1,and rest od the position should be set to 0.Hence your final output for this problem should be 1110000000000000000000000000000000000.


Output Example:

1110000000000000000000000000000000000



2.

Input Example:

Block Adventure Gildong is playing a video game called . In Block Adventure, there are n columns of blocks in a row, and the columns are numbered from 1 to n. All blocks have equal heights. The height of the i-th column is represented as h_i, which is the number of blocks stacked in the i-th column.Gildong plays the game as a character that can stand only on the top of the columns. At the beginning, the character is standing on the top of the 1-st column. The goal of the game is to move the character to the top of the n-th column.The character also has a bag that can hold infinitely many blocks. When the character is on the top of the i-th column, Gildong can take one of the following three actions as many times as he wants: In actions of the first two types the character remains in the i-th column, and the value h_i changes.The character initially has m blocks in the bag. Gildong wants to know if it is possible to win the game. Help Gildong find the answer to his question.

Reasoning:
Given the problem's context of Block Adventure game where Gildong aims to reach the last column by strategically adjusting column heights, we can infer that it involves both greedy strategy and mathematical calculations. The greedy strategy is needed to make optimal decisions at each step, while mathematical calculations are essential to assess the feasibility of reaching the last column with the given resources. Thus, the problem requires a combination of greedy strategy and mathematical reasoning.


Output Example:
0001100000000000000000000000000000000


3.

Input Example:

Round Corridor Amugae is in a very large round corridor. The corridor consists of two areas. The inner area is equally divided by n sectors, and the outer area is equally divided by m sectors. A wall exists between each pair of sectors of same area (inner or outer), but there is no wall between the inner area and the outer area. A wall always exists at the 12 o'clock position.The inner area's sectors are denoted as (1,1), (1,2), \dots, (1,n) in clockwise direction. The outer area's sectors are denoted as (2,1), (2,2), \dots, (2,m) in the same manner. For a clear understanding, see the example image above.Amugae wants to know if he can move from one sector to another sector. He has q questions.For each question, check if he can move between two given sectors.

Reasoning:
Given the problem's context of determining movement possibilities between sectors in the round corridor, we can deduce that it involves mathematical calculations and considerations related to the positioning of sectors. The task likely revolves around analyzing the numerical properties of sector positions to ascertain movement feasibility. This suggests an emphasis on mathematical reasoning rather than algorithmic complexities or specialized data structures.

Output Example:
0000011000000000000000000000000000000

    """
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
            ]
    )
    # print(completion.choices[0].message.content)
    return completion.choices[0].message.content



def read_specific_line(file_path, index):
    with open(file_path, 'r', encoding='utf-8') as tsvfile:
        for i, line in enumerate(tsvfile):
            if i == index:
                temp=line.strip().split('\t')
                temp.pop(0)
                return ''.join(temp)
            

def check(question_table,answer_table,q_index):
   
    question=read_specific_line(question_table,q_index)
    answer=read_specific_line(answer_table,q_index)

    response=ask(question)

    # print("answer,response")
    # print(answer)
    # print(response)
    # print("precision",precision(answer,response))
    # print("recall",recall(answer,response))
    # print("f1",f1(answer,response))
    #print("hamming_loss",hamming_loss(answer,response))
    return answer,response


avg_precision=0
avg_recall=0
avg_f1=0

for i in range(30):
    #avg_hamming_loss=0
    answer,response=check('ques.tsv','train+test+valid_100.tsv',20+2*i)
    avg_precision+=precision(answer,response)
    avg_recall+=recall(answer,response)
    avg_f1+=f1(answer,response)

print("avg_precision",avg_precision/20)
print("avg_recall",avg_recall/20)
print("avg_f1",avg_f1/20)


