mul	2	0	None
{
  "name":"R",
  "id":"%ID1%",
  "static":[
    {
      "name":"o",
      "id":"%ID2%",
      "static":["0"],
      "arguments":[
        {"no":0, "value":"IN0"},
        {"no":1, "value":"IN1"}
      ]
    },
    {
      "name":"i",
      "id":"%ID3%",
      "static":["2"],
      "arguments":[
        {"no":0, "value":"IN0"},
        {"no":1, "value":"IN1"},
        {"no":2, "value":{
          "name":"add",
          "id":"%ID4%",
          "static":[],
          "arguments":[
            {"no":0, "value":"IN2"},
            {"no":1, "value":"IN0"}
          ]
        }}
      ]
    }
  ],
  "arguments":[
     {"no":0, "value":%IN0%},
     {"no":1, "value":%IN1%}
  ]  
}
