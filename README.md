# 《哥德尔、艾舍尔、巴赫-集异璧之大成》中的程序
> 我们似乎很突然地从大脑和心智跳到了数学和计算机科学中。虽然这个跳跃从某些方面来看有点突然，但他还是有意义的。

这个仓库，我将尝试用Python来编写书中的例子以及推荐的练习，来进行读书笔记，以更好地理解形式化系统、印符系统甚至元数学。
## Chapter 13: BlooP和FlooP和GlooP
### Bloop_basic
这个文件中，基本仿造书中的伪代码，编写了Bloop的基本例子，这些都是“长度可预测的搜索”：
- \(2^{3^n}\) 
- 两个数相减
- 质数判断
- 哥德巴赫数

并且补充了质数判断必备的求余数函数。

### Bloop_advanced
这个文件编写的是书中推荐的练习题中数论相关的部分。

与WJU系统和TNT系统相关的待完成。

## Chapter 13: 自指与自复制
这一章里给了一个很有趣的印符遗传学例子，尝试实现如下：
### ImprintEnzyme.py
这个文件里实现了印符串（DNA）和印符酶（15种氨基酸的功能），可以实现15种氨基酸组成的印符酶对印符串的操作。

将会进一步完成印符串到印符酶的翻译，以及自复制系统。




# Programs in *Gödel, Escher, Bach: An Eternal Golden Braid*  
> It seems we’ve suddenly jumped from the topics of brain and mind to mathematics and computer science. While this leap may appear abrupt in some ways, it is nonetheless meaningful.  

In this repository, I will attempt to implement examples and recommended exercises from the book using Python as a way to take reading notes. This will help me better understand formal systems, symbol systems, and even metamathematics.  

## Chapter 13: BlooP, FlooP, and GlooP  
### Bloop_basic  
In this file, I have implemented basic examples of BlooP based on the book’s pseudocode. These are "predictably bounded searches":  
- \(2^{3^n}\)  
- Subtraction of two numbers  
- Prime number checking  
- Goldbach numbers  

Additionally, I included a modulus function essential for prime number checking.  

### Bloop_advanced  
This file contains implementations of number theory exercises recommended in the book.  

Tasks related to the WJU system and the TNT system are yet to be completed.

## Chapter 16: Self-Reference and Self-Replication  
This chapter introduces an intriguing example of symbolic genetics. The following will be implemented:  

### ImprintEnzyme.py  
This file implements operations on symbolic strings (DNA) and imprint enzymes (functions of 15 amino acids). It can simulate operations performed by enzymes composed of these 15 amino acids on DNA strings.  

Further work will include translating symbolic strings into enzymes and building a self-replicating system.  
