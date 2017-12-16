Parts Implemented by Burak Bekci
================================
Frontend of homepage and admin page, CRUD operations of Events and Drinks table, select, delete and update operations of Order table and achievement control.

Homepage
=========
Current events and news about restaurants, website and users are listed on this page. By clicking the event image user can go web page of each event.
Clicking names of the news will open their edit pages. However, this option is available for only admin.



Events Page
===========
Details of event, time and place of the event are shown on this page. Users who selected "Going" are listed at the bottom of the page.
Users can select "Going" or "Not Going" to that Event via a button. Admin can edit event via "Edit Event" button which is visible for admin only.


Admin Page
==========
In this page, admin can control everything. Restaurants, events, achievements, and users are listed so that admin can delete them.
By clicking the names of the achievements admin can edit an achievement. At the middle of the page, there is "message to user part". Admin can send a message
to any user. Below of it, there is a part for admin to publish a new. The published news will be listed on the homepage. At the bottom of the page, there are links for
creating events and achievements.


Event Create Form
=================
This page available for admin only.  All the information except "Potograph link of event" must given. Also "Starting Date of Event" must earlier than "Ending Date of Event".
Admin can open Event Edit form via Edit button on the Events page. Edit form is very similiar to Create form. The only difference is, in the Edit from there will be existing values of that Event.
