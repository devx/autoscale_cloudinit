#Rackspace Autoscale + cloudinit
This document covers Rackspace autoscale and cloudinit.  I will only cover the basic on creating a scaling group via curl.  The web GUI method has been covered before, you can find a good article about it here:

http://www.rackspace.com/blog/start-using-auto-scale-today/

##Overview
The product is offered for free to Rackspace customers, though you will still be charged for the cloud servers you utilize in scaling.

Setting up Auto Scale is simple as 1, 2, 3.

    1. Create a Scaling Group — a group of servers that will grow, or shrink, in number according to your rules.

    2. Create Scaling Rules using Monitoring – if you will use events rather than a schedule to trigger scaling — what thresholds or events to watch for (CPU load, queue length, req/sec, etc).

    3. Create a Scaling Policy— this defines how much to grow or shrink capacity.  For schedule-based scaling, you would also define when to do so. Rackspace Auto Scale will take care of the rest.  With a caveat for scale down there is no graceful action that get's taken when spinning down servers.


####Schedule-Based
If expect significant additional demand on your application at specific times. For example:

 * A holiday season sales boost on your e-commerce site
 * A major sales promotion on a specific day or for a period of time – ie. from a Super Bowl advertisement
 * During the day when more people are using your app, and during the night when most of your users are asleep

####Event-based
Monitoring your servers and detect that you need to add or reduce capacity based on the load. For example:

* Use Rackspace Cloud Monitoring to monitor individual server load and trigger a policy based on a threshold
* Use third party monitoring systems such as Nagios and trigger a policy based on a threshold
* Use Rackspace Cloud Monitoring with an available plug-in to monitor queue length and trigger a policy based on threshold



###Create a Scaling Group


First we will generate a auth token. If copying and pasting please modify the user name, and API key(aka password). Once it finishes you will generate a token, save that token as you will have to plug it in .
<pre><code>
curl -s -d\ '{ "auth": { "RAX-KSKEY:apiKeyCredentials": { "username": "MY USER NAME", "apiKey": "USER API KEY"} } }' \
    -H 'Content-Type: application/json'\
    'https://identity.api.rackspacecloud.com/v2.0/tokens'
</pre>
Next we will create an autoscale group that will spin up a maximum of 4 servers and minimum 1 server.  These servers are using the default Ubuntu 13.10 (Saucy Salamander) (PVHVM) performance server with 2Gig of ram. Additionally it will insert a ssh key that has been previously uploaded. Each of the servers will be created with a prepend name of 'test-au-'.

Make sure to change the following variables with the corresponding values MY_TENANT_ID, MY_AUTH_TOKEN and MY_SSH_KEY (this is the name of the ssh key that was uploaded)).


<pre><code>
curl -i https://ord.autoscale.api.rackspacecloud.com/v1.0/MY_TENANT_ID/groups -X POST -H 'X-Auth-Project-Id: MY_TENANT_ID' -H 'User-Agent: pyrax/1.7.0' -H 'Content-Type: application/json' -H 'Accept: application/json' -H 'X-Auth-Token: MY_AUTH_TOKEN' -d '
{
    "groupConfiguration": {
        "cooldown": 120,
        "maxEntities": 4,
        "metadata": {},
        "minEntities": 1,
        "name": "my_AutoScale_test1"
    },
    "launchConfiguration": {
        "args": {
            "server": {
                "OS-DCF:diskConfig" : "MANUAL",
                "config_drive" : true,
                "flavorRef": "performance1-2",
                "imageRef": "6110edfe-8589-4bb1-aa27-385f12242627",
                "key_name" : "MY_SSH_KEY",
                "user_data" : "I2Nsb3VkLWNvbmZpZwoKcGFja2FnZXM6CgogLSBhcGFjaGUyCiAtIHBocDUKIC0gcGhwNS1teXNxbAogLSBteXNxbC1zZXJ2ZXIKCnJ1bmNtZDoKCiAtIHdnZXQgaHR0cDovL3dvcmRwcmVzcy5vcmcvbGF0ZXN0LnRhci5neiAtUCAvdG1wLwogLSB0YXIgLXp4ZiAvdG1wL2xhdGVzdC50YXIuZ3ogLUMgL3Zhci93d3cvCiAtIG15c3FsIC1lICJjcmVhdGUgZGF0YWJhc2Ugd29yZHByZXNzOyBjcmVhdGUgdXNlciAnd3B1c2VyJ0AnbG9jYWxob3N0JyBpZGVudGlmaWVkIGJ5ICdjaGFuZ2VtZXRvbyc7IGdyYW50IGFsbCBwcml2aWxlZ2VzIG9uIHdvcmRwcmVzcyAuIFwqIHRvICd3cHVzZXInQCdsb2NhbGhvc3QnOyBmbHVzaCBwcml2aWxlZ2VzOyIKIC0gbXlzcWwgLWUgImRyb3AgZGF0YWJhc2UgdGVzdDsgZHJvcCB1c2VyICd0ZXN0J0AnbG9jYWxob3N0JzsgZmx1c2ggcHJpdmlsZWdlczsiCiAtIG15c3FsYWRtaW4gLXUgcm9vdCBwYXNzd29yZCAnY2hhbmdlbWUnCg==",
                "name": "test-au-"
            }
        },
        "type": "launch_server"
    },
    "scalingPolicies": []
}'
</pre>

Once this finishes(assuming everything worked and there were no errors) you should be able to view it on the cloud  portal.  It should also kick off a server that will execute the following cloud init config.
<pre><code>
#cloud-config

packages:

 - apache2
 - php5
 - php5-mysql
 - mysql-server

runcmd:

 - wget http://wordpress.org/latest.tar.gz -P /tmp/
 - tar -zxf /tmp/latest.tar.gz -C /var/www/
 - mysql -e "create database wordpress; create user 'wpuser'@'localhost' identified by 'changemetoo'; grant all privileges on wordpress . \* to 'wpuser'@'localhost'; flush privileges;"
 - mysql -e "drop database test; drop user 'test'@'localhost'; flush privileges;"
 - mysqladmin -u root password 'changeme'
</pre>

One important thing to note is that the "user_data" used for server creation needs to be encoded in a b64 format.  I have included two quick scripts that will encode and decode the file.

<pre><code>

</code></pre>
#cloud-init


There is a great article that talks about using cloud-init with rackspace cloud and you can find it below.

#####Links:
http://developer.rackspace.com/blog/using-cloud-init-with-rackspace-cloud.html

http://docs.rackspace.com/servers/api/v2/cs-devguide/content/Create_Server_with_configdrive.html



##Troubleshooting cloud-init
This is a good segue into what happens if something goes wrong and you need to figure out what exploded.

Log files can typically be found in /var/log/cloud-init.log.

The copy of your cloud-config is stored here: /var/lib/cloud/instance/cloud-config.txt.

The /var/lib/cloud directory also has other useful information, such as files that let cloud-init know it’s already run once so you can rest easy cloud-init isn’t going to setup Apache again if you reboot your server

