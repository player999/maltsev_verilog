add	2	0	None
{
	"name":"R",
	"id":"%ID1%",
	"static":[
	{
		"name":"i",
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
				"name":"s",
				"id":"%ID4%",
				"static":[],
				"arguments":[
					{"no":0, "value":"IN2"}
				]
				}
			}
		]
	}
	],
	"arguments":[
		{"no":0, "value":%IN0%},
		{"no":1, "value":%IN1%}
	] 
}
