import java.util.Scanner;

public class Main{
    public static void main(String[] argv) {
        System.out.println(convert(Scale.FARENHEIT, 212));
        System.out.println(convert(Scale.CELCIUS, 100));
    }

    enum Scale {
        CELCIUS, FARENHEIT
    }

    static float convert(Scale type, float num){
        if (type == Scale.CELCIUS){
            return (num * 9/5) + 32;
        }
        else {
            return (num - 32) * 5/9;
        }
    }
}

