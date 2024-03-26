# def sort_file(file_path):
#     with open(file_path, 'r', newline='') as file:
#         header = file.readline().strip().split('\t')  # 读取头部信息
#         data = [line.strip().split('\t') for line in file]
#     sorted_data = sorted(data, key=lambda x: int(x[0]))  # 根据第一列进行排序
#     return header, sorted_data

# def merge_sorted_files(file1_path, file2_path, output_path):
#     header1, sorted_data1 = sort_file(file1_path)
#     header2, sorted_data2 = sort_file(file2_path)

#     with open(output_path, 'w', newline='') as output_file:
#         output_file.write('\t'.join(header1) + '\n')  # 写入头部信息

#         index1 = index2 = 0
#         while index1 < len(sorted_data1) and index2 < len(sorted_data2):
#             if int(sorted_data1[index1][0]) < int(sorted_data2[index2][0]):
#                 output_file.write('\t'.join(sorted_data1[index1]) + '\n')
#                 index1 += 1
#             else:
#                 output_file.write('\t'.join(sorted_data2[index2]) + '\n')
#                 index2 += 1

#         # 写入剩余的数据
#         while index1 < len(sorted_data1):
#             output_file.write('\t'.join(sorted_data1[index1]) + '\n')
#             index1 += 1
#         while index2 < len(sorted_data2):
#             output_file.write('\t'.join(sorted_data2[index2]) + '\n')
#             index2 += 1


def merge_sorted_files(file1_path, file2_path, output_path):
    with open(file1_path, 'r') as file1, open(file2_path, 'r') as file2, open(output_path, 'w') as output_file:
        data1 = [line.strip().split('\t') for line in file1]
        data2 = [line.strip().split('\t') for line in file2]

        merged_data = sorted(data1 + data2, key=lambda x: int(x[0]))

        for row in merged_data:
            output_file.write('\t'.join(row) + '\n')

# 调用合并函数
merge_sorted_files('train.tsv', 'test.tsv', 'train+test.tsv')
merge_sorted_files('train+test.tsv', 'valid.tsv', 'train+test+valid.tsv')


def truncate(file_path,output_path,n):
    #截取一部分行
    with open(file_path, 'r', newline='') as file:
        header = file.readline().strip().split('\t')  # 读取头部信息
        data = [line.strip().split('\t') for line in file]
    truncated_data = data[:n]
    with open(output_path, 'w', newline='') as output_file:
        output_file.write('\t'.join(header) + '\n')  # 写入头部信息
        for line in truncated_data:
            output_file.write('\t'.join(line) + '\n')



# 调用合并函数
# merge_sorted_files('train.tsv', 'test.tsv', 'train+test.tsv')
# merge_sorted_files('train+test.tsv', 'valid.tsv', 'train+test+valid.tsv')
truncate('train+test+valid.tsv','train+test+valid_100.tsv',100)