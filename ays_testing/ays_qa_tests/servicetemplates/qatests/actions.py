from JumpScale import j


class Actions(ActionsBaseMgmt):
    def install(self, service):
        print("Hello I'm running JS8 TESTS...")
        host = service.hrd.getStr('host')
        cmd = service.hrd.getStr('testcmd')

        executer = j.tools.executor.getSSHViaProxy(host)
        connection=executer.cuisine

        def clone_repo(directory):
            a = connection.core.run("%s; ls"%directory)[1].find('org_quality')
            if a < 0:
                connection.core.run("%s; git clone https://js-awesomo:jsR00t3r@"
                                    "github.com/gig-projects/org_quality.git" %directory)

        clone_repo('cd')
        clone_repo('cd /opt/code/github/')
        mail_service = service.getProducers('mailclient')[0]
        email_sender = mail_service.actions.getSender(mail_service)

        rc, out, err = connection.core.run(cmd)
        email_sender.send(service.hrd.getStr('sendto'),
                          mail_service.hrd.getStr("smtp.sender"),
                          "asdadad",
                          "OUT: %s, ERR: %s"%(out, err),
                          'html',
                          )






