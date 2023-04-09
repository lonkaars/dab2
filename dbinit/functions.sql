use `formula1`;	
drop function if exists udfTotalDistance;

delimiter $$
create function udfTotalDistance(raceID int)
returns int
begin
	return (
		select `circuit`.`length` * `circuit`.`laps`
		from `race`
		inner join `circuit` on `circuit`.`ID` = `race`.`circuitID`
		where `race`.`ID` = raceID);
end$$

delimiter ;
