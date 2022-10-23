SELECT allee, "libellésous-famille" as ss_famille, d3.total3 as expired, d2.total2 AS less_5_days, count(*) as more_5_days
FROM donneesApp as d1 
JOIN donneesExtraites on ean = reference_id 
full OUTER JOIN (SELECT COUNT(*) as total2, allee as allee2, "libellésous-famille" as lib2 FROM donneesApp 
           JOIN donneesExtraites on ean = reference_id
			WHERE libellégroupedefamille = "CHARCUTERIE"
	  		AND (JULIANDAY("expiry_date") - JULIANDAY('2020-10-20')) < 5
      		and (JULIANDAY("expiry_date") - JULIANDAY('2020-10-20')) > 0 
      		group by allee2, lib2) as d2 on (allee = allee2 and ss_famille = lib2)
FULL OUTER JOIN (SELECT COUNT(*) as total3, allee as allee3, "libellésous-famille" as lib3 FROM donneesApp 
           JOIN donneesExtraites as dE on ean = reference_id
			WHERE libellégroupedefamille = "CHARCUTERIE"
	  		AND (JULIANDAY("expiry_date") - JULIANDAY('2020-10-20')) < 0
      		group by allee3, lib3) as d3 on (allee = allee3 and ss_famille = lib3)

Where libellégroupedefamille = "CHARCUTERIE"
and (JULIANDAY("expiry_date") - JULIANDAY('2020-10-20')) > 5
group by allee, ss_famille
ORDER by expired DESC
;