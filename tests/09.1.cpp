// !test number_overflow

#include<iostream> // суязвимостью
usingnamespacestd;

int main()
{
    int a = 0;
    int d = 45445678765431;
    for (int i = 0; i < 1000; i++)
    {
        a += 3342315000000;   
    }
    return 0;
}