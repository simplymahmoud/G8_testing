# The GIG quality process
our GIG quality process is an intergral part of the [development process.](https://gig.gitbooks.io/agile/content/CodingCycle.html)

# Which test should be performed

There are 8 main testing items defined that need to be in place in order to have a stable product. All of those test should be performed by the quality team 

1. Installation testing → Currently done by Ops team.  
The quality team should be able to perform fresh installations from an environment. The role of operations in this matter should be limited to setting up and installing the controller and network.  

2. Upgrade testing → Now done by the Ops team
The quality team should be able to perform upgrades from an environment. There should not be any envolvement of operations in this matter.

3. JumpScale testing → should be done by the quality team (un-tested so far)
Automated tests of the Jumpscale core modules which are regurlary used should be tested on functionality in automated tests.

4. Portal testing → Now done by quality team
All user portals should be tested so that we are not receiving unexpected errors.

5. API automated testing → Now done by quality team
Automated tests should be written in order to assure good functionality of the API's

6. Security testing → Now done by quality team (need specialised recourses)
Our roduct should have a decent security level, automated and manual test should be performed in order to achieve this.

7. Performance testing → Now done by quality team
Performance tests should be written in order to check the boundaries of our system.

8. Sanity testing → Done by our internal healthchecker
Good function of the healthchecker of a system should be assured.
