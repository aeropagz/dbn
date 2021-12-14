-- Create view 
-- Welche Alben sind am längsten hinsichtlich der Abspieldauer? Nachrangiges Sortierkriterium sei die Anzahl der Titel der Alben.


CREATE VIEW longest_alboms AS
SELECT sum(length), album.title FROM song
JOIN album on album.id = album_id
GROUP BY album_id;