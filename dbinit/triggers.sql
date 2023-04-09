drop trigger if exists endposition_ai;
drop trigger if exists endposition_ad;
drop trigger if exists endposition_au;
-- drop trigger if exists fastestlap_ai;
-- drop trigger if exists fastestlap_ad;
-- drop trigger if exists fastestlap_au;

delimiter $$
create trigger endposition_ai after insert on endposition
for each row begin
	insert into `formula1`.`auditlog` (`action`, `fieldName`, `newData`)
		select 'insert', 'endposition.memberID', cast(new.`memberID` as char)
		from `endposition` as d where d.`ID` = new.`ID`;
	insert into `formula1`.`auditlog` (`action`, `fieldName`, `newData`)
		select 'insert', 'endposition.position', cast(new.`position` as char)
		from `endposition` as d where d.`ID` = new.`ID`;
	insert into `formula1`.`auditlog` (`action`, `fieldName`, `newData`)
		select 'insert', 'endposition.specialPositionID', cast(new.`specialPositionID` as char)
		from `endposition` as d where d.`ID` = new.`ID`;
end; $$
delimiter ;

delimiter $$
create trigger endposition_ad before delete on endposition
for each row begin
	insert into `formula1`.`auditlog` (`action`, `fieldName`, `newData`)
		select 'delete', 'endposition.memberID', NULL
		from `endposition` as d where d.`ID` = old.`ID`;
	insert into `formula1`.`auditlog` (`action`, `fieldName`, `newData`)
		select 'delete', 'endposition.position', NULL
		from `endposition` as d where d.`ID` = old.`ID`;
	insert into `formula1`.`auditlog` (`action`, `fieldName`, `newData`)
		select 'delete', 'endposition.specialPositionID', NULL
		from `endposition` as d where d.`ID` = old.`ID`;
end; $$
delimiter ;

delimiter $$
create trigger endposition_au after update on endposition
for each row begin
	insert into `formula1`.`auditlog` (`action`, `fieldName`, `newData`)
		select 'update', 'endposition.memberID', cast(new.`memberID` as char)
		from `endposition` as d where d.`ID` = new.`ID` and old.`memberID` != new.`memberID`;
	insert into `formula1`.`auditlog` (`action`, `fieldName`, `newData`)
		select 'update', 'endposition.position', cast(new.`position` as char)
		from `endposition` as d where d.`ID` = new.`ID` and old.`position` != new.`position`;
	insert into `formula1`.`auditlog` (`action`, `fieldName`, `newData`)
		select 'update', 'endposition.specialPositionID', cast(new.`specialPositionID` as char)
		from `endposition` as d where d.`ID` = new.`ID` and old.`specialPositionID` != new.`specialPositionID`;
end; $$
delimiter ;


-- delimiter $$
-- create trigger fastestlap_ai after insert on fastestlap
-- for each row begin
-- 	insert into `formula1`.`auditlog` (`action`, `fieldName`, `newData`)
-- 		select 'insert', 'fastestlap.memberID', cast(new.`memberID` as char)
-- 		from `fastestlap` as d where d.`ID` = new.`ID`;
-- end; $$
-- delimiter ;
-- 
-- delimiter $$
-- create trigger fastestlap_ad before delete on fastestlap
-- for each row begin
-- 	insert into `formula1`.`auditlog` (`action`, `fieldName`, `newData`)
-- 		select 'delete', 'fastestlap.memberID', NULL
-- 		from `fastestlap` as d where d.`ID` = old.`ID`;
-- end; $$
-- delimiter ;
-- 
-- delimiter $$
-- create trigger fastestlap_au after update on fastestlap
-- for each row begin
-- 	insert into `formula1`.`auditlog` (`action`, `fieldName`, `newData`)
-- 		select 'update', 'fastestlap.memberID', cast(new.`memberID` as char)
-- 		from `fastestlap` as d where d.`ID` = new.`ID` and old.`memberID` != new.`memberID`;
-- end; $$
-- delimiter ;
