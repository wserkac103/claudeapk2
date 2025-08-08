package com.example.twobuttonsapp;

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.Toast;

public class MainActivity extends AppCompatActivity {

    private Button button1;
    private Button button2;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // Find buttons by their ID
        button1 = findViewById(R.id.button1);
        button2 = findViewById(R.id.button2);

        // Set OnClickListener for the first button
        button1.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                // Show a toast message
                Toast.makeText(MainActivity.this, R.string.toast_message_1, Toast.LENGTH_SHORT).show();
            }
        });

        // Set OnClickListener for the second button
        button2.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                // Show a different toast message
                Toast.makeText(MainActivity.this, R.string.toast_message_2, Toast.LENGTH_SHORT).show();
            }
        });
    }
}
