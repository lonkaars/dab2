drop procedure if exists spUpdateFlags;

delimiter $$
create procedure spUpdateFlags(imgPath varchar(255))
	begin
		update `nationality` as `A`
		set `A`.`flag` = (
			select load_file(concat(imgPath, `country`, ".png")) as `flag`
			from `nationality` as `B`
			where `B`.`ID` = `A`.`ID`);
	end$$
delimiter ;
