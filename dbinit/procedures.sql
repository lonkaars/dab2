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

drop procedure if exists spDeleteFlags;

delimiter $$
create procedure spDeleteFlags()
	begin
		update `nationality`
		set `nationality`.`flag` = NULL
		where `nationality`.`flag` is not NULL
	end$$
delimiter ;
