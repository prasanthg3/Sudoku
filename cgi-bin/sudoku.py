import cgi, cgitb
from pulp import *
cgitb.enable()

# Create instance of FieldStorage 
form = cgi.FieldStorage() 

vals=rows=cols = [str(x) for x in range(1,10)]
       
prob = LpProblem("Sudoku",LpMaximize)

x = LpVariable.dicts("x",(vals,rows,cols),0,1,LpInteger)

for r in rows:
    for c in cols:
        prob += lpSum([x[v][r][c] for v in vals]) == 1, ""

squares =[]
for i in range(3):
    for j in range(3):
        squares += [[(rows[3*i+k],cols[3*j+l]) for k in range(3) for l in range(3)]]
        
for v in vals:
    for r in rows:
        prob += lpSum([x[v][r][c] for c in cols]) == 1,""
        
    for c in cols:
        prob += lpSum([x[v][r][c] for r in rows]) == 1,""

    for b in squares:
        prob += lpSum([x[v][r][c] for (r,c) in b]) == 1,""

ind=[[b,f] for b in range(1,10) for f in range(1,10)]                                  
for i in range(81):
    if form.getvalue("cell-{0}".format(i))!= None:
        prob += x[form.getvalue("cell-{0}".format(i))][str(ind[i][0])][str(ind[i][1])] == 1,""
prob.writeLP("sudoku.lp")
prob.solve()

sol=[v for v in vals for c in cols for r in rows if value(x[v][r][c])==1]
if len(sol)==81:
    print('''
	<html lang="en">
    <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    
    <title>Sudoku</title>
    
    <link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css" rel="stylesheet">
    
    <style type="text/css">
    
      html, body {
        background-color: #FAFAFA
      }
      table {
        border: 2px solid #000000;
      }
      td {
        border: 1px solid #000000;
        text-align: center;
        vertical-align: middle;  
      }
      input[type=text] {
        color: #000000;
        padding: 0;
        border: 0;
        text-align: center;
        width: 48px;
        height: 48px;
        font-size: 24px;
        background-color: #FFFFFF;
        outline: none;
      }
	  input[type=button]{
       padding:15px 25px; 
		background:#00cc00;
		font-size: 24px;
		border:0 none;
		cursor:pointer;
		-webkit-border-radius: 5px;
		border-radius: 5px;
      }
	  
      input:disabled {
        background-color: #EEEEEE;
      }
      #cell-0,  #cell-1,  #cell-2  { border-top:    2px solid #000000; }
      #cell-2,  #cell-11, #cell-20 { border-right:  2px solid #000000; }
      #cell-18, #cell-19, #cell-20 { border-bottom: 2px solid #000000; }
      #cell-0,  #cell-9,  #cell-18 { border-left:   2px solid #000000; }
      #cell-3,  #cell-4,  #cell-5  { border-top:    2px solid #000000; }
      #cell-5,  #cell-14, #cell-23 { border-right:  2px solid #000000; }
      #cell-21, #cell-22, #cell-23 { border-bottom: 2px solid #000000; }
      #cell-3,  #cell-12, #cell-21 { border-left:   2px solid #000000; }
      #cell-6,  #cell-7,  #cell-8  { border-top:    2px solid #000000; }
      #cell-8,  #cell-17, #cell-26 { border-right:  2px solid #000000; }
      #cell-24, #cell-25, #cell-26 { border-bottom: 2px solid #000000; }
      #cell-6,  #cell-15, #cell-24 { border-left:   2px solid #000000; }
      #cell-27, #cell-28, #cell-29 { border-top:    2px solid #000000; }
      #cell-29, #cell-38, #cell-47 { border-right:  2px solid #000000; }
      #cell-45, #cell-46, #cell-47 { border-bottom: 2px solid #000000; }
      #cell-27, #cell-36, #cell-45 { border-left:   2px solid #000000; }
      #cell-30, #cell-31, #cell-32 { border-top:    2px solid #000000; }
      #cell-32, #cell-41, #cell-50 { border-right:  2px solid #000000; }
      #cell-48, #cell-49, #cell-50 { border-bottom: 2px solid #000000; }
      #cell-30, #cell-39, #cell-48 { border-left:   2px solid #000000; }
      #cell-33, #cell-34, #cell-35 { border-top:    2px solid #000000; }
      #cell-35, #cell-44, #cell-53 { border-right:  2px solid #000000; }
      #cell-51, #cell-52, #cell-53 { border-bottom: 2px solid #000000; }
      #cell-33, #cell-42, #cell-51 { border-left:   2px solid #000000; }
      #cell-54, #cell-55, #cell-56 { border-top:    2px solid #000000; }
      #cell-56, #cell-65, #cell-74 { border-right:  2px solid #000000; }
      #cell-72, #cell-73, #cell-74 { border-bottom: 2px solid #000000; }
      #cell-54, #cell-63, #cell-72 { border-left:   2px solid #000000; }
      #cell-57, #cell-58, #cell-59 { border-top:    2px solid #000000; }
      #cell-59, #cell-68, #cell-77 { border-right:  2px solid #000000; }
      #cell-75, #cell-76, #cell-77 { border-bottom: 2px solid #000000; }
      #cell-57, #cell-66, #cell-75 { border-left:   2px solid #000000; }
      #cell-60, #cell-61, #cell-62 { border-top:    2px solid #000000; }
      #cell-62, #cell-71, #cell-80 { border-right:  2px solid #000000; }
      #cell-78, #cell-79, #cell-80 { border-bottom: 2px solid #000000; }
      #cell-60, #cell-69, #cell-78 { border-left:   2px solid #000000; }
    </style>
  </head>
  <body>
	
    <div class="container" align="center">
      
      <h1> Solution </h1>
   
      <form action = "./cgi-bin/sudoku.py" method = "POST">

	  <table id="grid" align="center">

        <tr>
          <td><input id="cell-0"  type="text" disabled value="''',[a for a in vals if value(x[a]['1']['1'])==1][0],'''" ></td>
          <td><input id="cell-1"  type="text"  disabled value="''',[a for a in vals if value(x[a]['1']['2'])==1][0],'''" > </td>
          <td><input id="cell-2"  type="text"  disabled value="''',[a for a in vals if value(x[a]['1']['3'])==1][0],'''"></td>
          
          <td><input id="cell-3"  type="text"  disabled value="''',[a for a in vals if value(x[a]['1']['4'])==1][0],'''"></td>
          <td><input id="cell-4"  type="text"  disabled value="''',[a for a in vals if value(x[a]['1']['5'])==1][0],'''" ></td>
          <td><input id="cell-5"  type="text"  disabled value="''',[a for a in vals if value(x[a]['1']['6'])==1][0],'''"></td>
          
          <td><input id="cell-6"  type="text"  disabled value="''',[a for a in vals if value(x[a]['1']['7'])==1][0],'''"></td>
          <td><input id="cell-7"  type="text"  disabled value="''',[a for a in vals if value(x[a]['1']['8'])==1][0],'''"></td>
          <td><input id="cell-8"  type="text"  disabled value="''',[a for a in vals if value(x[a]['1']['9'])==1][0],'''"></td>
        </tr>

        <tr>
          <td><input id="cell-9"  type="text"  disabled value="''',[a for a in vals if value(x[a]['2']['1'])==1][0],'''" ></td>
          <td><input id="cell-10" type="text"  disabled value="''',[a for a in vals if value(x[a]['2']['2'])==1][0],'''"></td>
          <td><input id="cell-11" type="text"  disabled value="''',[a for a in vals if value(x[a]['2']['3'])==1][0],'''"></td>
          
          <td><input id="cell-12" type="text"  disabled value="''',[a for a in vals if value(x[a]['2']['4'])==1][0],'''"></td>
          <td><input id="cell-13" type="text"  disabled value="''',[a for a in vals if value(x[a]['2']['5'])==1][0],'''"></td>
          <td><input id="cell-14" type="text"  disabled value="''',[a for a in vals if value(x[a]['2']['6'])==1][0],'''"></td>
          
          <td><input id="cell-15" type="text"  disabled value="''',[a for a in vals if value(x[a]['2']['7'])==1][0],'''"></td>
          <td><input id="cell-16" type="text"  disabled value="''',[a for a in vals if value(x[a]['2']['8'])==1][0],'''"></td>
          <td><input id="cell-17" type="text"  disabled value="''',[a for a in vals if value(x[a]['2']['9'])==1][0],'''"></td>
        </tr>

        <tr>          
          <td><input id="cell-18" type="text"  disabled value="''',[a for a in vals if value(x[a]['3']['1'])==1][0],'''"></td>
          <td><input id="cell-19" type="text"  disabled value="''',[a for a in vals if value(x[a]['3']['2'])==1][0],'''"></td>
          <td><input id="cell-20" type="text"  disabled value="''',[a for a in vals if value(x[a]['3']['3'])==1][0],'''"></td>
          
          <td><input id="cell-21" type="text"  disabled value="''',[a for a in vals if value(x[a]['3']['4'])==1][0],'''"></td>
          <td><input id="cell-22" type="text"  disabled value="''',[a for a in vals if value(x[a]['3']['5'])==1][0],'''"></td>
          <td><input id="cell-23" type="text"  disabled value="''',[a for a in vals if value(x[a]['3']['6'])==1][0],'''"></td>
          
          <td><input id="cell-24" type="text"  disabled value="''',[a for a in vals if value(x[a]['3']['7'])==1][0],'''"></td>
          <td><input id="cell-25" type="text"  disabled value="''',[a for a in vals if value(x[a]['3']['8'])==1][0],'''" ></td>
          <td><input id="cell-26" type="text"  disabled value="''',[a for a in vals if value(x[a]['3']['9'])==1][0],'''"></td>
        </tr>

        <tr>          
          <td><input id="cell-27" type="text"  disabled value="''',[a for a in vals if value(x[a]['4']['1'])==1][0],'''" ></td>
          <td><input id="cell-28" type="text"  disabled value="''',[a for a in vals if value(x[a]['4']['2'])==1][0],'''"></td>
          <td><input id="cell-29" type="text"  disabled value="''',[a for a in vals if value(x[a]['4']['3'])==1][0],'''"></td>
          
          <td><input id="cell-30" type="text"  disabled value="''',[a for a in vals if value(x[a]['4']['4'])==1][0],'''"></td>
          <td><input id="cell-31" type="text"  disabled value="''',[a for a in vals if value(x[a]['4']['5'])==1][0],'''" ></td>
          <td><input id="cell-32" type="text"  disabled value="''',[a for a in vals if value(x[a]['4']['6'])==1][0],'''"></td>
          
          <td><input id="cell-33" type="text"  disabled value="''',[a for a in vals if value(x[a]['4']['7'])==1][0],'''"></td>
          <td><input id="cell-34" type="text"  disabled value="''',[a for a in vals if value(x[a]['4']['8'])==1][0],'''"></td>
          <td><input id="cell-35" type="text"  disabled value="''',[a for a in vals if value(x[a]['4']['9'])==1][0],'''"></td>
        </tr>

        <tr>          
          <td><input id="cell-36" type="text"  disabled value="''',[a for a in vals if value(x[a]['5']['1'])==1][0],'''"></td>
          <td><input id="cell-37" type="text"  disabled value="''',[a for a in vals if value(x[a]['5']['2'])==1][0],'''"></td>
          <td><input id="cell-38" type="text"  disabled value="''',[a for a in vals if value(x[a]['5']['3'])==1][0],'''"></td>
          
          <td><input id="cell-39" type="text"  disabled value="''',[a for a in vals if value(x[a]['5']['4'])==1][0],'''" ></td>
          <td><input id="cell-40" type="text"  disabled value="''',[a for a in vals if value(x[a]['5']['5'])==1][0],'''"></td>
          <td><input id="cell-41" type="text"  disabled value="''',[a for a in vals if value(x[a]['5']['6'])==1][0],'''" ></td>
          
          <td><input id="cell-42" type="text"  disabled value="''',[a for a in vals if value(x[a]['5']['7'])==1][0],'''"></td>
          <td><input id="cell-43" type="text"  disabled value="''',[a for a in vals if value(x[a]['5']['8'])==1][0],'''"></td>
          <td><input id="cell-44" type="text"  disabled value="''',[a for a in vals if value(x[a]['5']['9'])==1][0],'''" ></td>
        </tr>

        <tr>          
          <td><input id="cell-45" type="text"  disabled value="''',[a for a in vals if value(x[a]['6']['1'])==1][0],'''" ></td>
          <td><input id="cell-46" type="text"  disabled value="''',[a for a in vals if value(x[a]['6']['2'])==1][0],'''"></td>
          <td><input id="cell-47" type="text"  disabled value="''',[a for a in vals if value(x[a]['6']['3'])==1][0],'''"></td>
          
          <td><input id="cell-48" type="text"  disabled value="''',[a for a in vals if value(x[a]['6']['4'])==1][0],'''"></td>
          <td><input id="cell-49" type="text"  disabled value="''',[a for a in vals if value(x[a]['6']['5'])==1][0],'''" ></td>
          <td><input id="cell-50" type="text"  disabled value="''',[a for a in vals if value(x[a]['6']['6'])==1][0],'''"></td>
          
          <td><input id="cell-51" type="text"  disabled value="''',[a for a in vals if value(x[a]['6']['7'])==1][0],'''"></td>
          <td><input id="cell-52" type="text"  disabled value="''',[a for a in vals if value(x[a]['6']['8'])==1][0],'''"></td>
          <td><input id="cell-53" type="text"  disabled value="''',[a for a in vals if value(x[a]['6']['9'])==1][0],'''" ></td>
        </tr>

        <tr>          
          <td><input id="cell-54" type="text"  disabled value="''',[a for a in vals if value(x[a]['7']['1'])==1][0],'''"></td>
          <td><input id="cell-55" type="text"  disabled value="''',[a for a in vals if value(x[a]['7']['2'])==1][0],'''" ></td>
          <td><input id="cell-56" type="text"  disabled value="''',[a for a in vals if value(x[a]['7']['3'])==1][0],'''"></td>
          
          <td><input id="cell-57" type="text"  disabled value="''',[a for a in vals if value(x[a]['7']['4'])==1][0],'''"></td>
          <td><input id="cell-58" type="text"  disabled value="''',[a for a in vals if value(x[a]['7']['5'])==1][0],'''"></td>
          <td><input id="cell-59" type="text"  disabled value="''',[a for a in vals if value(x[a]['7']['6'])==1][0],'''"></td>
          
          <td><input id="cell-60" type="text"  disabled value="''',[a for a in vals if value(x[a]['7']['7'])==1][0],'''"></td>
          <td><input id="cell-61" type="text"  disabled value="''',[a for a in vals if value(x[a]['7']['8'])==1][0],'''" ></td>
          <td><input id="cell-62" type="text"  disabled value="''',[a for a in vals if value(x[a]['7']['9'])==1][0],'''"></td>
        </tr>

        <tr>          
          <td><input id="cell-63" type="text"  disabled value="''',[a for a in vals if value(x[a]['8']['1'])==1][0],'''"></td>
          <td><input id="cell-64" type="text"  disabled value="''',[a for a in vals if value(x[a]['8']['2'])==1][0],'''"></td>
          <td><input id="cell-65" type="text"  disabled value="''',[a for a in vals if value(x[a]['8']['3'])==1][0],'''"></td>
          
          <td><input id="cell-66" type="text"  disabled value="''',[a for a in vals if value(x[a]['8']['4'])==1][0],'''" ></td>
          <td><input id="cell-67" type="text"  disabled value="''',[a for a in vals if value(x[a]['8']['5'])==1][0],'''" ></td>
          <td><input id="cell-68" type="text"  disabled value="''',[a for a in vals if value(x[a]['8']['6'])==1][0],'''" ></td>
          
          <td><input id="cell-69" type="text"  disabled value="''',[a for a in vals if value(x[a]['8']['7'])==1][0],'''"></td>
          <td><input id="cell-70" type="text"  disabled value="''',[a for a in vals if value(x[a]['8']['8'])==1][0],'''"></td>
          <td><input id="cell-71" type="text"  disabled value="''',[a for a in vals if value(x[a]['8']['9'])==1][0],'''" ></td>
        </tr>

        <tr>          
          <td><input id="cell-72" type="text"  disabled value="''',[a for a in vals if value(x[a]['9']['1'])==1][0],'''"></td>
          <td><input id="cell-73" type="text"  disabled value="''',[a for a in vals if value(x[a]['9']['2'])==1][0],'''"></td>
          <td><input id="cell-74" type="text"  disabled value="''',[a for a in vals if value(x[a]['9']['3'])==1][0],'''"></td>
          
          <td><input id="cell-75" type="text"  disabled value="''',[a for a in vals if value(x[a]['9']['4'])==1][0],'''"></td>
          <td><input id="cell-76" type="text"  disabled value="''',[a for a in vals if value(x[a]['9']['5'])==1][0],'''" ></td>
          <td><input id="cell-77" type="text"  disabled value="''',[a for a in vals if value(x[a]['9']['6'])==1][0],'''"></td>
          
          <td><input id="cell-78" type="text"  disabled value="''',[a for a in vals if value(x[a]['9']['7'])==1][0],'''"></td>
          <td><input id="cell-79" type="text"  disabled value="''',[a for a in vals if value(x[a]['9']['8'])==1][0],'''" ></td>
          <td><input id="cell-80" type="text"  disabled value="''',[a for a in vals if value(x[a]['9']['9'])==1][0],'''" ></td>
        </tr>

      </table>
	  <br>
<form>
  <input type="button" value="Try Again!" onclick="history.back()" align="center">
</form>
    </div>
	
		
  </body>
</html>''')
else:
    print('''
		<html lang="en">
    <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
<title>Solution</title>
<link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css" rel="stylesheet">
    
    <style type="text/css">
    
      html, body {
        background-color: #FAFAFA
      }
      
    
	  input {
       padding:15px 25px; 
		background:#00cc00;
		font-size: 24px;
		border:0 none;
		cursor:pointer;
		-webkit-border-radius: 5px;
		border-radius: 5px;
        align:center;
      }
	  
      input:disabled {
        background-color: #EEEEEE;
      }
	  </style>
</head>
<body>
<div align ="center">
<h1 align="center" style="color:#FAFAFA;">No Solution</h1>
<h1 align="center" style="color:#FAFAFA;">No Solution</h1>
<h1 align="center" style="color:#FAFAFA;">No Solution</h1>
<h1 align="center" style="color:Tomato;">No Solution</h1>
<h1 align="center" style="color:#FAFAFA;">No Solution</h1>
<h1 align="center" style="color:#FAFAFA;">No Solution</h1>
<h1 align="center" style="color:#FAFAFA;">No Solution</h1>
<form align="center">
  <input type="button" value="Try Again!" onclick="history.back()" align="center">
</form>
</div>
</body>
</html>''')


    
    