function massimo_subarray(a) {
	/*
	* Some work here; return type and arguments should be according to the problem's requirements
	*/
	var l = a.length;
	var sub_array;
	var massimo_intermedio;
	var maximum_sum = a[0];
	
	function myFunction(total, value, index, array) {
		return total + value;
	}
	
	for (s=1; s<=l; s++) {
		for (p=0; p<=l-s; p++) {
			sub_array = a.slice(p,p+s);
			massimo_intermedio = sub_array.reduce(myFunction);
			if (massimo_intermedio > maximum_sum) {
				maximum_sum = massimo_intermedio;
			}
		}
	}
	return maximum_sum;
}

// SI PUO' FARE ANCHE RAGGRUPPANDO A MANO A MANO GLI ADIACENTI POSITIVI
<!DOCTYPE html>
<html>
<body>

<p>massimo subarray</p>

<script>
  var a = [-2,1,2,-4,13,23];
  var l = a.length;
  var sub_array;
  var massimo_intermedio;
  var maximum_sum = a[0];

  function myFunction(total, value, index, array) {
    return total + value;
  }

  for (var s=1; s<=l; s++) {
    for (var p=0; p<=l-s; p++) {
      sub_array = a.slice(p,p+s);
      massimo_intermedio = sub_array.reduce(myFunction);
      document.write(s," ",p,"..... ",sub_array,"<br>");
      // document.write(s+' '+p+' '+subarray+' '+massimo_intermedio+' '+maximum_sum+'\n');
      if (massimo_intermedio > maximum_sum) {
        maximum_sum = massimo_intermedio;
      }
    }
  }
  document.write(maximum_sum)
  
</script>

</body>
</html>
