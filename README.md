# Homeless-PhD-waiting-for-PGH
This is for CUHK RPGs on the PGH waiting list to avoid checking website from time to time:
Automatically check PGH website every day and send you a email if there is any updates on waiting list.

Some variables that you have to change:
send_smtp, send_port, send_address, send_password: information of email sender.
receive_address: address of the email receiver.
sid: CUHK student ID.
N: N=1 if you want to see how many person left on the original waiting list. Save the original waiting list as "source.txt".
check_time: string of the checking time, like '18:00' or '00:00'.
pgh_link: for year 20-21 is 'http://www.pgh.cuhk.edu.hk/announcements/2020/Pending.php'.

Notice: 
It might require additional settings of your sender email. for gmail, you need to turn on "Less secure app access". The CUHK email is not recommended because you cannot do changes to your account.
If you are male, you should delete 2 lines in the script.

Edith Z 21/01/2021
