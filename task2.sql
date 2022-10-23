SELECT count(*) as expired, 
	(SELECT  COUNT(*) FROM donneesApp
	  WHERE (JULIANDAY("expiry_date") - JULIANDAY('2020-10-20')) < 5
      and (JULIANDAY("expiry_date") - JULIANDAY('2020-10-20')) > 0 )
     AS less_5_days, 
	(SELECT  COUNT(*) FROM donneesApp
	  WHERE (JULIANDAY("expiry_date") - JULIANDAY('2020-10-20')) > 5 )
     as more_5_days
FROM donneesApp 
WHERE (JULIANDAY("expiry_date") - JULIANDAY('2020-10-20')) < 0
;