package cp213;
import java.util.Scanner;

public class Testing {

    public static void main(String[] args) {
		System.out.print("hello");
        Scanner myObj = new Scanner(System.in);  // Create a Scanner object
    	System.out.print("Enter a string: ");
		String s = myObj.nextLine();
        Boolean result = isPalindrome(s);
		myObj.close();
		System.out.println();
        System.out.println(result);
		System.out.println();
    }

    /**
     * Determines if s is a palindrome. Ignores case, spaces, digits, and
     * punctuation in the string parameter s.
     *
     * @param s
     *            a string
     * @return true if s is a palindrome, false otherwise
     */
    public static boolean isPalindrome(final String s) {
    	
     	boolean isP = false; 
     	int checkP = 0;
     	int iterator = 0;
     	char fromStartChar; 
     	char fromEndChar; 
     	String allAlpha = ""; 
     	char currentChar; 
    	
     	//Make a new string (allAlpha) containing only letters (no spaces) 
     	//Check if capital. If not make it a capital. 
     	for (int i = 0; i < s.length(); ++i) { 
     		currentChar = s.charAt(i); 
     		if (Character.isLetter(currentChar)) {
     			allAlpha = allAlpha + Character.toTitleCase(currentChar); 
     		}
     	}
     	
     	//If empty string or one character it is a palindrome: 
    	if (allAlpha.length() <= 1) {
    		isP = true; 
    	}
    	//If not empty or one character we need to compare. 
    	else { 
    		while (checkP == 0 && iterator < allAlpha.length()) {
    			fromStartChar = allAlpha.charAt(iterator);
    			fromEndChar = allAlpha.charAt(allAlpha.length() - 1 - iterator);
    			if (fromStartChar != fromEndChar) {
    				checkP = -1; 
    				isP = false;
    			}
    			else { 
    				iterator += 1; 
    			}
    			if (iterator >= allAlpha.length() / 2) {
    				isP = true;
    			}
    		}
    	}
    	return isP;
    	}
    }