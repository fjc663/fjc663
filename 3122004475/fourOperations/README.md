| 这个作业属于哪个课程 | [软件工程](https://edu.cnblogs.com/campus/gdgy/CSGrade22-34)                |
|------------|-------------------------------------------------------------------------|
| 这个作业要求在哪里  |  |
| 这个作业的目标    |  |

---

## 一、我的作业github链接

[https://github.com/fjc663/fjc663/tree/main/3122004475/fourOperations](https://github.com/fjc663/fjc663/tree/main/3122004475/fourOperations)

---

## 二、PSP表

| PSP2.1                                       | Personal Software Process Stages | 预估耗时（分钟） | 实际耗时（分钟） |
|----------------------------------------------|----------------------------------|----------|----------|
| **Planning**                                  | 计划                               |          |          |
| **Estimate**                                  | 估计这个任务需要多少时间                     |          |          |
| **Development**                               | 开发                               |          |          |
| - Analysis                                    | - 需求分析 (包括学习新技术)                 |          |          |
| - Design Spec                                 | - 生成设计文档                         |          |          |
| - Design Review                               | - 设计复审                           |          |          |
| - Coding Standard                             | - 代码规范 (为目前的开发制定合适的规范)           |          |          |
| - Design                                      | - 具体设计                           |          |          |
| - Coding                                      | - 具体编码                           |          |          |
| - Code Review                                 | - 代码复审                           |          |          |
| - Test                                        | - 测试（自我测试，修改代码，提交修改）             |          |          |
| **Reporting**                                 | 报告                               |          |          |
| - Test Report                                 | - 测试报告                           |          |          |
| - Size Measurement                            | - 计算工作量                          |          |          |
| - Postmortem & Process Improvement Plan       | - 事后总结, 并提出过程改进计划                |          |          |
|                                   | **合计**                           | **??**   | **??**   |

---

## 三、效能分析

![函数用时分析](./images/fourOperStatistics.png)


---

## 四、设计实现过程


---


## 五、代码说明


---

## 六、测试运行

### 测试用例 1：生成 10 个四则运算题目，数值范围为 10
```bash
python script.py -n 10 -r 10
```
**期望结果**: 生成 10 个题目并保存在 Exercises.txt，对应答案保存在 Answers.txt。

### 测试用例 2：生成 5 个四则运算题目，数值范围为 100
```bash
python script.py -n 5 -r 100
```
**期望结果**: 生成 5 个题目并保存在 Exercises.txt，题目中的数字在 1 到 100 之间。

### 测试用例 3：验证生成的答案
```bash
python script.py -e Exercises.txt -a Answers.txt
```
**期望结果**: 验证 Exercises.txt 和 Answers.txt 中的题目与答案是否匹配，正确和错误统计保存在 Grade.txt。

### 测试用例 4：数值范围为 1（无效范围）
```bash
python script.py -n 5 -r 1
```
**期望结果**: 输出错误提示 "Error: 范围应大于 1"，不会生成题目。



### 为什么程序是正确的

- **运算正确性**: 程序使用 fractions.Fraction 确保了分数计算的准确性，避免了浮点数计算误差。
- **错误处理**: 通过处理 ZeroDivisionError 和数值范围限制，避免了非法运算。
- **验证结果**: 自动生成的题目和答案已经通过匹配验证，确保了输出答案的准确性。
- **格式化输出**: 程序对分数和带分数进行了正确的格式化，并验证了这些格式化结果是否符合预期。


---


## 七、项目小结