package com.example.esercizio_003imieiinteressi;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

public class DataProvider {
    public static HashMap<String, List<String>> getInfo(){

        HashMap<String, List<String>> HeaderDetails = new HashMap<String, List<String>>();
        List<String> ChildDetails1 = new ArrayList<String>();
        ChildDetails1.add("primo figlio");
        ChildDetails1.add("secondo figlio");
        List<String> ChildDetails2 = new ArrayList<String>();
        ChildDetails2.add("eccomi!");
        ChildDetails2.add("barbablu");
        ChildDetails2.add("tra la la");

        HeaderDetails.put("Capo 1", ChildDetails1);
        HeaderDetails.put("Capo 2", ChildDetails2);

        return HeaderDetails;
    }
}
