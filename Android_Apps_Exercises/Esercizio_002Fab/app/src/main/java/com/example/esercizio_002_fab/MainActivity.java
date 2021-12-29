package com.example.esercizio_002_fab;

import android.content.Intent;
import android.os.Bundle;
import androidx.appcompat.app.AppCompatActivity;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.ListView;
//import android.widget.TextView;
//import android.widget.Toast;

public class MainActivity extends AppCompatActivity {
    ListView lv;
    //TextView textView;
    String[] lista = {"Fab1",
            "Fab2",
            "Fab3",
            "Fab4",
            "Fab5",
            "Fab6",
            "Fab7",
            "Fab8",
            "Fab9",
            "Fab10",
            "Fab11",
            "Fab12",
            "Fab13",
            "Fab14"
    };

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        lv = (ListView) findViewById(R.id.idListView);
        ArrayAdapter<String> adapter = new ArrayAdapter<String>(this, android.R.layout.simple_list_item_1, lista);
        lv.setAdapter(adapter);
        lv.setOnItemClickListener(new AdapterView.OnItemClickListener() {

            @Override
            public void onItemClick(AdapterView<?> adapterView, View view, int i, long l) {
                //Toast.makeText(getApplicationContext(),"Elemento selezionato: "+(i+1),Toast.LENGTH_SHORT).show();
                //textView = (TextView) findViewById(R.id.idtxt);
                Intent j  = new Intent(getApplicationContext(), Main2Activity.class);
                startActivity(j);
            }

            ;
        });
    }
}