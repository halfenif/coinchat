
SHELL=/bin/bash
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/local/games:/usr/games
HOME=/home/pi





DROP TABLE public.tb_chat;

CREATE TABLE public.tb_chat
(
    daystr text  NOT NULL,
    timestr text  NOT NULL,
    uid text  NOT NULL,
    msg text  NOT NULL,
    regdate timestamp with time zone NOT NULL,
    CONSTRAINT tb_chat_pkey PRIMARY KEY (daystr, timestr, uid, msg)
)
;


ALTER TABLE public.tb_chat
    ALTER COLUMN regdate SET DEFAULT now();
