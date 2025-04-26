#include <stdio.h>
#include <stdlib.h>

int first_ind(int ar[], int n){ //������� ������ ������� ������� �������� � �������
    int res;
    for (int i = 0 ; i < n; i++){
        if(ar[i]%2 == 0){
           res = i;
              return res;
        }
    }

}

int last_ind(int ar[], int n){  // ������� ������ ���������� ������� �������� � �������
    int res;
    for (int i = n; i > 0; i--){
         if(ar[i]%2 == 1){
           res = i;
            return res;
        }
    }
}

int abssum_betwen(int ar[], int n){ //������� ����� ������� ���������, ������� ����� ������ ������ � ��������� �������� ��-�� � �������, ������� ������ � �� ������� ������
  int first = first_ind(ar, n);
  int last = last_ind(ar, n);
  int abssum = 0;
  for (int i = first; i < last; i++){
            abssum += abs(ar[i]);
        }
        return abssum;
}

int abssum_bef_aft(int ar[], int n){    //������� ����� ������� ���������, ������� �� ������� ��������, �� ������� ��� � ��������� ����� ���������� �������, ������� ���
        int abssum = 0;
        int first = first_ind(ar, n);
        int last = last_ind(ar, n);
        for (int i = 0; i < first; i++){
            abssum +=  abs(ar[i]);
        }
        for (int i = last; i < n; i++){
            abssum += abs(ar[i]);
        }
        return abssum;
}

int main()
{
     int ar[100];
     int cs;
     int n = 0;
     char c;
     scanf("%d%c", &cs, &c); // ���� ������� �����, ������������� ���������� �������� ���������
     while(n<100){              // ���� �������
            scanf("%d%c",&ar[n],&c);
            n++;
            if(c == '\n'){
                break;
            }
     }

    int res = 0;
    switch(cs){
case 0:
   printf("%d\n", first_ind(ar, n));

    break;

case 1:
   printf("%d\n", last_ind(ar,n));
   break;

case 2:

    res = abssum_betwen(ar, n);
    printf("%d\n", res);

    break;

case 3:
    res = abssum_bef_aft(ar, n);
    printf("%d\n", res);

    break;

default:
    printf("������ �����������");

    }
return 0;
}


