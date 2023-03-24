drop function if exists udfTotalDistance;

delimiter $$
create function udfTotalDistance(raceID int)
returns int
begin
	return (
		select `circuit`.`length` * `circuit`.`laps`
		from `circuit`
		inner join `racedatecircuit` on `racedatecircuit`.`circuitID` = `circuit`.`ID`
		inner join `racedate` on `racedate`.`ID` = `racedatecircuit`.`raceDateID`
		inner join `race` on `race`.`raceDateID` = `racedate`.`ID`
		where `race`.`ID` = raceID);
end$$

delimiter ;
