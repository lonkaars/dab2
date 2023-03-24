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
		where `nationality`.`flag` is not NULL;
	end$$
delimiter ;

drop procedure if exists spUpdatePersons;

delimiter $$
create procedure spUpdatePersons(imgPath varchar(255))
	begin
		select concat(imgPath, regexp_replace(concat(`firstName`, " ", `middleName`, " ", `lastName`), '  *', ' '), ".jpg") from `member`;
		update `member` as `A`
		set `A`.`photo` = (
			select load_file(concat(imgPath, regexp_replace(concat(`firstName`, " ", `middleName`, " ", `lastName`), '  *', ' '), ".jpg")) as `photo`
			from `member` as `B`
			where `B`.`ID` = `A`.`ID`);
	end$$
delimiter ;

