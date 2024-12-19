from enum import Enum
from typing import List


# 定义氨基酸类型
class AminoAcid(Enum):
    CUT = "cut"    # 切割DNA串
    DEL = "del"    # 删除碱基
    SWI = "swi"    # 把酶转移到另一个串上
    MVR = "mvr"    # 右移一个单元
    MVL = "mvl"    # 左移一个单元
    COP = "cop"    # 进入复制状态
    OFF = "off"    # 退出复制状态
    INA = "ina"    # 在本单元右侧插入A
    INC = "inc"    # 在本单元右侧插入C
    ING = "ing"    # 在本单元右侧插入G
    INT = "int"    # 在本单元右侧插入T
    RPY = "rpy"    # 寻找右边最近的嘧啶T/C
    RPU = "rpu"    # 寻找右边最近的嘌呤A/G
    LPY = "lpy"    # 寻找左边最近的嘧啶T/C
    LPU = "lpu"    # 寻找左边最近的嘌呤A/G
    

class DNA:
    def __init__(self, sequence: str):
        if not all(base in 'ACGT ' for base in sequence):
            raise ValueError(f"DNA序列只能包含ACGT，发现非法字符在序列: {sequence}")
        self.sequence = sequence
    
    def validate(self) -> bool:
        """验证DNA序列是否合法"""
        return all(base in 'ACGT ' for base in self.sequence) #包含了空格
    
    def __str__(self):
        return self.sequence
    
    def __repr__(self):
        return f"DNA('{self.sequence}')"

class Enzyme:
    def __init__(self, amino_acids: List[AminoAcid]):
        self.amino_acids = amino_acids
        self.position = 0  # 酶在DNA上的位置
        self.is_copying = False  # 是否处于复制状态
        self.copy_string = ''  # 复制串
        self.on_original = True  # True表示在原始串上，False表示在复制串上

    
    def attach(self, position: int):
        """将酶附着在DNA的特定位置"""
        self.position = position
    
    def get_complement(self, base: str) -> str:
        """获取碱基的互补碱基"""
        complements = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
        return complements[base]
    
    def copy_current_position(self, result: str, current_pos: int):
        """复制当前位置的碱基到复制串"""
        if current_pos >= len(result):
            return
        
        # 计算在复制串中的对应位置（倒序）
        copy_pos = len(result) - current_pos - 1
        
        # 如果复制串长度不够，用空格填充
        while len(self.copy_string) < len(result):
            self.copy_string += ' '
        
        # 如果该位置还没有复制过，则进行复制
        if self.copy_string[copy_pos] == ' ':
            complement = self.get_complement(result[current_pos])
            self.copy_string = (
                self.copy_string[:copy_pos] + 
                complement + 
                self.copy_string[copy_pos + 1:]
            )
    
    def visualize_state(self, result: str, current_pos: int, amino: AminoAcid):
        """可视化当前DNA处理状态"""
        # 计算最大行宽
        width = max(len(result), len(self.copy_string)) + 4
        
        print("\n" + "=" * width)
        print(f"当前氨基酸: {amino.value}")
        print(f"当前位置在: {'原始串' if self.on_original else '复制串'}")
        print("-" * width)
        
        # 创建位置指示器
        if (self.on_original):
            position_marker = " " * current_pos + "^"
        else:
            position_marker = " " * (len(result) - current_pos - 1) + "^"
        
        if self.on_original:
            print("原始串: " + result)
            print("位置  : " + position_marker)
            if self.is_copying:
                # 复制串倒序显示
                reversed_copy = ''.join(reversed(self.copy_string))
                print("复制串: " + reversed_copy)
        else:
            # 当在复制串上时，显示顺序相反
            reversed_result = ''.join(reversed(result))
            print("复制串: " + reversed_result)
            print("位置  : " + position_marker)
            print("原始串: " + self.copy_string)
        
        print("=" * width + "\n")
    
    def process(self, dna: DNA, visualize_on:bool=1) -> List[DNA]:
        result = dna.sequence
        current_pos = self.position
        
        # 处理所有氨基酸操作
        for amino in self.amino_acids:
        # for i, amino in enumerate(self.amino_acids):
            if (visualize_on):
                self.visualize_state(result, current_pos, amino)
            
            if amino == AminoAcid.COP and not self.is_copying:
                # 进入复制状态
                self.is_copying = True
                self.copy_string = ' ' * len(result)
                # 首先复制当前位置
                self.copy_current_position(result, current_pos)
                continue
            
            # 在复制状态下执行其他操作
            elif amino == AminoAcid.OFF:
                # 退出复制状态
                self.is_copying = False
                final_copy = self.copy_string.replace(' ', '')
                return [DNA(result), DNA(final_copy)]
            # # 在复制状态下执行其他操作
            # if self.is_copying:
            #     if amino == AminoAcid.OFF:
            #         # 退出复制状态
            #         self.is_copying = False
            #         final_copy = self.copy_string.replace(' ', '')
            #         return [DNA(result), DNA(final_copy)]
            #     # # 其他操作继续正常执行，但要确保复制当前位置
            #     # self.copy_current_position(result, current_pos)
            
            # ... 其他操作的处理保持不变 ...
            elif amino == AminoAcid.CUT:
                left = DNA(result[:current_pos+1])
                right = DNA(result[current_pos+1:])
                if self.is_copying:
                    # 对复制串也进行切割
                    copy_pos = len(result) - current_pos - 1
                    copy_left = DNA(self.copy_string[:copy_pos].replace(' ', ''))
                    copy_right = DNA(self.copy_string[copy_pos:].replace(' ', ''))
                    return [left, right, copy_left, copy_right]
                return [left, right]
            
            elif amino in [AminoAcid.MVR, AminoAcid.MVL, AminoAcid.RPY, AminoAcid.RPU, 
                          AminoAcid.LPY, AminoAcid.LPU]:
                # 移动操作
                old_pos = current_pos
                if amino == AminoAcid.MVR:
                    current_pos = min(current_pos + 1, len(result) - 1)
                elif amino == AminoAcid.MVL:
                    current_pos = max(current_pos - 1, 0)
                elif amino == AminoAcid.RPY:
                    # 向右寻找最近的嘧啶(T/C)
                    for i in range(current_pos + 1, len(result)):
                        if result[i] in 'TC':
                            current_pos = i
                            break
                elif amino == AminoAcid.RPU:
                    # 向右寻找最近的嘌呤(A/G)
                    for i in range(current_pos + 1, len(result)):
                        if result[i] in 'AG':
                            current_pos = i
                            break
                elif amino == AminoAcid.LPY:
                    # 向左寻找最近的嘧啶(T/C)
                    for i in range(current_pos - 1, -1, -1):
                        if result[i] in 'TC':
                            current_pos = i
                            break
                elif amino == AminoAcid.LPU:
                    # 向左寻找最近的嘌呤(A/G)
                    for i in range(current_pos - 1, -1, -1):
                        if result[i] in 'AG':
                            current_pos = i
                            break
                
                if self.is_copying:
                    # 复制移动过的所有位置
                    for pos in range(min(old_pos, current_pos), max(old_pos, current_pos) + 1):
                        self.copy_current_position(result, pos)
            
            elif amino in [AminoAcid.INA, AminoAcid.INC, AminoAcid.ING, AminoAcid.INT]:
                # 插入操作
                # 获取要插入的碱基，amino.value[-1] 表示获取氨基酸值的最后一个字符（即要插入的碱基），并确保为大写
                base_to_insert = amino.value[-1].upper()
                result = result[:current_pos+1] + base_to_insert + result[current_pos+1:]
                if self.is_copying:
                    # 在复制串对应位置插入互补碱基
                    complement = self.get_complement(base_to_insert)
                    copy_pos = len(self.copy_string) - current_pos - 1
                    self.copy_string = (
                        self.copy_string[:copy_pos] + 
                        complement + 
                        self.copy_string[copy_pos:]
                    )
                current_pos += 1
            
            # elif amino == AminoAcid.SWI:
            #     if self.is_copying:
            #         # 计算在复制串中的对应位置
            #         copy_pos = len(result) - current_pos - 1
            #         # 检查该位置是否有碱基
            #         if self.copy_string[copy_pos] == ' ':
            #             return DNA(result)  # 如果位置无效，退出处理
                    
            #         # 切换到复制串
            #         self.is_copying = False
            #         self.on_original = False
            #         current_pos = copy_pos  # 直接使用计算出的复制串位置
            #         # 交换原始串和复制串，保留空格
            #         result, self.copy_string = self.copy_string, result
            #     elif not self.on_original:
            #         # 从复制串切换回原始串
            #         self.on_original = True
            #         # 计算在原始串中的对应位置
            #         current_pos = len(result) - current_pos - 1
            #         # 交换回原始串和复制串
            #         result, self.copy_string = self.copy_string, result
            #     else:
            #         # 如果不在复制状态且在原始串上，忽略该操作
            #         continue
            elif amino == AminoAcid.SWI:
                if self.on_original:
                    # 计算在复制串中的对应位置
                    copy_pos = len(result) - current_pos - 1
                    # 检查该位置是否有碱基
                    if self.copy_string[copy_pos] == ' ':
                        return DNA(result)  # 如果位置无效，退出处理
                    
                    # 切换到复制串
                    # self.is_copying = False
                    self.on_original = False
                    current_pos = copy_pos  # 直接使用计算出的复制串位置
                    # 交换原始串和复制串，保留空格
                    result, self.copy_string = self.copy_string, result
                else: 
                    # 从复制串切换回原始串
                    self.on_original = True
                    # 计算在原始串中的对应位置
                    current_pos = len(result) - current_pos - 1
                    # 交换回原始串和复制串
                    result, self.copy_string = self.copy_string, result
        
        # 所有操作执行完后，如果仍在复制状态，继续向右复制到末尾
        if self.is_copying:
            for pos in range(current_pos + 1, len(result)):
                self.copy_current_position(result, pos)
        # 只在最终返回时去除空格
        final_copy = self.copy_string.replace(' ', '')
        final_result = result.replace(' ', '')
        return [DNA(final_result), DNA(final_copy)]
            
        # return DNA(result)
    
    @classmethod
    def from_string(cls, pattern: str):
        """从字符串创建酶，例如 'mov-cut-ins'"""
        actions = pattern.split('-')
        amino_acids = []
        
        # 将字符串转换为对应的枚举值
        for action in actions:
            try:
                amino_acid = AminoAcid(action.lower())
                amino_acids.append(amino_acid)
            except ValueError:
                raise ValueError(f"无效的氨基酸类型: {action}")
                
        return cls(amino_acids)

# 使用示例
def main():
    # dna = DNA("CAAAGAGAATCCTCTTTGAT")
    # print(f"原始DNA: {dna}")    
    # enzyme = Enzyme.from_string("rpy-cop-rpu-cut")
    # enzyme.attach(2)  # 初始在第2个A

    # dna = DNA("ATGC")
    # print(f"原始DNA: {dna}")    
    # enzyme = Enzyme.from_string("cop-mvr-off")
    # enzyme.attach(0)  # 初始在第2个A

    # dna = DNA("TAGATCCAGTCCATCGA")
    # print(f"原始DNA: {dna}")    
    # enzyme = Enzyme.from_string("rpu-inc-cop-mvr-mvl-swi-lpu-int")
    # enzyme.attach(8)  # 初始在第2个A

    dna = DNA("TAGATCCAGTCCATCGA")
    print(f"原始DNA: {dna}")    
    enzyme = Enzyme.from_string("rpu-inc-cop-mvr-mvl-swi-lpu-int-swi-ing")
    enzyme.attach(8)  # 初始在第2个A

    
    result = enzyme.process(dna)
    if isinstance(result, list):
        print(f"处理后的DNA片段: {', '.join(str(d) for d in result)}")
    else:
        print(f"处理后的DNA: {result}")

if __name__ == "__main__":
    main()

