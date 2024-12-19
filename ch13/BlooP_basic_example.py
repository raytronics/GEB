def two_to_the_three_to_two(n):
    # BLOCK0 BEGIN
    cell_0 = 1;                   
    for i in range(1,n+1):   
        # BLOCK1 BEGIN 
        cell_0= 3 * cell_0;
        # BLOCK1 END
    cell_1 = 1;                   
    for i in range (1,cell_0+1):  
        # BLOCK2 BEGIN 
        cell_1 = 2*cell_1; 
        # BLOCK2 END  
    output = cell_1;
    # BLOCK0 END  
    return output;



# print(two_to_the_three_to_two(2));


def minus(m,n):
    #BLOCK0 BEGIN
    if(m<n):
        output = 0;
    #QUIT BLOCK0
    else:
        for i in range (0,m+1):
            #BLOCK1 BEGIN
            if (i+n==m):
                output=i;
                break;
            #BLOCK1 END
    #BLOCK0 END
    return output;

# print(minus(3,3));

def remainder(m,n): # M/N的余数
    if(m<n):
        output = 0;
    else:
        for i in range (1,m+1):
            #BLOCK1 BEGIN
            if (i*n<=m and (i+1)*n>m):
                output=minus(m,i*n);
                break;
            #BLOCK1 END
    return output;

print(remainder(4,2));

def prime(n):
    if(n<=1):
        output = False;
    elif (n==2):
        output = True;
    else:
        cell_0=2;
        for i in range(1,minus(n,2)+1):
            if remainder(n,cell_0)==0:
                output= False;
                break;
            else:
                cell_0 = cell_0 + 1;
            output = True;
    return output;

# for i in range(0,200):
#     print(f"{i} 的质数检查结果是 {prime(i)}")

def goldbach(n):
    output=False;
    cell_0 = 2;
    for i in range(1,n+1):
        if (prime(cell_0) and prime(minus(n,cell_0))):
            output = True;
            break;
        else:
            cell_0 = cell_0 + 1;
    return output,cell_0,minus(n,cell_0)


for i in range(0,200,2):
    result = goldbach(i)
    print(f"{i} 等于 {result[1]} 和 {result[2]}这两个质数的和")


