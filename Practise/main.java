import java.util.*;

interface fileSystem {
    void ls();
}

class File implements fileSystem {
    String fileName;

    public File(String name) {this.fileName  = name;}

    public void ls(){
        System.out.println("file name" + fileName); 
    }
}
public class main {
    public static void main(String[] args) {

    }
}
