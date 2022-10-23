SELECT allee, d3.total3 as expired, d2.total2 AS less_5_days, count(*) as more_5_days
FROM donneesApp as d1 
Full OUTER join (SELECT COUNT(*) as total2, allee as allee2 FROM donneesApp 
	  WHERE (JULIANDAY("expiry_date") - JULIANDAY('2020-10-20')) < 5
      and (JULIANDAY("expiry_date") - JULIANDAY('2020-10-20')) > 0 
      group by allee2) as d2 on allee = allee2
full OUTER join (SELECT COUNT(*) as total3, allee as allee3 FROM donneesApp 
	  		WHERE (JULIANDAY("expiry_date") - JULIANDAY('2020-10-20')) < 0
      		group by allee3) as d3 on allee = allee3
WHERE (JULIANDAY("expiry_date") - JULIANDAY('2020-10-20')) > 5
group by allee
ORDER by expired DESC
;