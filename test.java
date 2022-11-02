class Test{
    public static void main(String[] args) {
        int k = 0;
        try {
            for(int i = 1; i<=5; i++){
                for(int j = 1; j<=3; j++){
                    if(i == j || i == 3 || i+j == 8){
                        if(i == 3){
                            for(int l = i + 2; l >= 3 ; l--){
                                System.out.print(l);
                            }
                            k = i + 2;
                        }
                        else{
                            k = k+1;
                            System.out.print(k);
                        }
                    }
                    else{
                        System.out.print(" ");
                    }
                }
                System.out.println();
            }
            
        } catch (Exception e) {
            System.out.println(e);
        }
    }
}
// 1
//  2
// 543
//  6
//   7