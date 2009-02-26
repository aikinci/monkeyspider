--$Id$

-- db scheme for monkey-spider
DROP TABLE mw_output;
DROP TABLE malware;
DROP TABLE mw_scanner;

CREATE TABLE malware (
	id		int		PRIMARY KEY,	--uniqe malware-id
	filename	varchar(40),	--filename of the malware
	url		text,		-- UNIQUE,	--url where it was crawled
	checksum	varchar(32),	--checksum 
	size		int,		--filesize
	date		timestamp,	--date when the file was crawled
	comment		varchar(20)     --comment
);

CREATE TABLE mw_scanner (
	id		int 		PRIMARY KEY, 	--uniqe malware-scanner-id
	name		varchar(20),	--name of the malwarescanner
	engine_ver	varchar(40),	--the engine version 
	signature_ver	varchar(40),    --the signature version
	lastupdate	timestamp,	--date when the mw-scanner was last updated
	UNIQUE		(engine_ver,signature_ver)
);

CREATE TABLE mw_output (
	mw_id		int		REFERENCES malware(id),		--foreign key to malware.id
	mw_sc_id	int		REFERENCES mw_scanner(id),	--foreign key to mw_scanner.id
	description	varchar(20),	--description of the found malware
	PRIMARY KEY (mw_id,mw_sc_id)	--Primary key are the both foreign keys
);

