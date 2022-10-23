SELECT count(*) - (SELECT COUNT(*) from donneesExtraites 
					JOIN donneesApp on ean = reference_id
					WHERE "Datedéréf." IS NULL
					AND "DateDebCad." IS NOT NULL
					AND "Stockenquantité" IS NOT NULL
					AND CAST("Stockenquantité" AS FLOAT) > 0) 
FROM donneesExtraites 
WHERE "Datedéréf." IS NULL
AND "DateDebCad." IS NOT NULL
AND "Stockenquantité" IS NOT NULL
AND CAST("Stockenquantité" AS FLOAT) > 0
;

