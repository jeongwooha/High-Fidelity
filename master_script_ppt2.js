// master_script_ppt2.js
// last updated 2/20/17 by JeongWoo Ha
// for HiFi Study


// THIS IS THE SRIPT FOR PPT2 ONLY


/*

    HiFi study domain | stanford.highfidelity.io

    Avatar Links updated |

    Male Bodied: https://s3-us-west-2.amazonaws.com/vhilhifi/male_body.fst
    Male Disembodied: https://s3-us-west-2.amazonaws.com/vhilhifi/male_hands.fst
    Female Bodied: https://s3-us-west-2.amazonaws.com/vhilhifi/female_body.fst
    Female Disembodied: https://s3-us-west-2.amazonaws.com/vhilhifi/female_hands.fst


    Avatar Positions |

    PPT1: 7.5, 31, 0
    PPT2: 3.7, 31, 0
*/



/*-------------------------------------------------------------------------*/
/*  Keypress:                                                              */
/*  m - display counter                                                    */
/*  b - display wall                                                       */
/*  c - countdown the counter                                              */
/*  r - rest the counter to 20                                             */
/*  v - start the 5 minute countdown and the wall shows up again           */
/*  f - fix the arm movement                                               */
/*                                                                         */
/*  z - start sending data                                                 */
/*  x - stop sending data                                                  */
/*                                                                         */
/*-------------------------------------------------------------------------*/


function overrideAnims() {
    var excludedRoles = ["rightHandGraspOpen",
                         "rightHandGraspClosed",
                         "leftHandGraspOpen",
                         "leftHandGraspClosed"];

    var IDLE_URL = "http://hifi-content.s3.amazonaws.com/ozan/dev/anim/standard_anims_160127/idle.fbx";

    var skeletonModelURL = MyAvatar.skeletonModelURL;
    var jointCount = MyAvatar.jointNames.length;
    var roles = MyAvatar.getAnimationRoles();
    var length = roles.length;

    for (var i = 0; i < length; i++) {
        if (excludedRoles.indexOf(roles[i]) == -1) {
            // override all the avatar motions into IDLE motion
            MyAvatar.overrideRoleAnimation(roles[i], IDLE_URL, 30, false, 1, 1);
        }
    }
}

// update motion every second manually
var t = 0;
function update(dt) {
    t += dt;
    if (t > 1) {
        overrideAnims();
        t = 0;
    }
}

overrideAnims();

Script.update.connect(update);
Script.scriptEnding.connect(function () {
    Script.update.disconnect(update);
})


// Enable/disable visibility of the wall
// 'b'
var wall = '5af10887-444c-4283-928d-059644ca36e8';
var visible = Entities.getEntityProperties(wall, visible);

Controller.keyPressEvent.connect(function(key) {
    print("you pressed " + key.text);
    if (key.text === 'b') {
        visible = !visible;
        Entities.editEntity(wall, {visible: visible});
        print("wall visibility");
    }
});


// Countdown the count by 1
// 'c'
var numtext1 = 'bd153e01-3247-433a-b06d-023f2c435851'; // for PPT2 avatar
var numtext2 = 'ca72b2d1-f0ce-47b8-9a49-1525bc076a55'; // for PPT1 avatar

var num = 20;

Entities.editEntity(numtext1, {text: num});
Entities.editEntity(numtext2, {text: num});


Controller.keyPressEvent.connect(function(key) {
    if (key.text === 'c') {
        if (num > 0) {
            num--;
        }

        Entities.editEntity(numtext1, {text: num});
        Entities.editEntity(numtext2, {text: num});
        print("countdown by 1");
    }
});


// Reset the counter to 20
// 'r'
Controller.keyPressEvent.connect(function(key) {
    if (key.text === 'r') {
        num = 20;
        Entities.editEntity(numtext1, {text: num});
        Entities.editEntity(numtext2, {text: num});
        print("counter reseted to 20");
    }
});


// Enable/disable visibility for numtext1 and numtext2
// 'm'
var visible_counter = Entities.getEntityProperties(numtext1, visible);

Controller.keyPressEvent.connect(function(key) {
    if (key.text === 'm') {
        visible_counter = !visible_counter;
        Entities.editEntity(numtext1, {visible: visible_counter});
        Entities.editEntity(numtext2, {visible: visible_counter});
        print("counter visibility");
    }
});


// After 5 minutes, the wall will come back up
// 'v'
Controller.keyPressEvent.connect(function(key) {
    if (key.text === 'v') {
        visible = !visible;
        Entities.editEntity(wall, {visible: visible}); // make the wall dissapear
        Script.setTimeout(function () {
            Entities.editEntity(wall, {visible: !visible});
        }, 300000);
        print("5 minute timer starting now...")

        // if (!visible) {
        //     Entities.editEntity(wall, {visible: visible});
        // } else {
        //     Script.setTimeout(function () {
        //         Entities.editEntity(wall, {visible: visible});
        //     }, 300000); // 300000 milliseconds = 5 minutes
        //     print("v timer starting...");
        // }
    }
});


// 'connected' text to show the data is being sent to DyanmoDB
var connected = 'd2fa1432-b361-48e0-a801-2cb60586be31';
var connectedVisible = Entities.getEntityProperties(connected, visible);

//var numtext1Color = Entities.getEntityProperties(numtext1, textColor);
//var numtext2Color = Entities.getEntityProperties(numtext2, textColor);

// When pressed 'z', start sending data and pop up the 'connected' sign in the room
Controller.keyPressEvent.connect(function(key) {
    print("you pressed " + key.text);

    // make the countdown numbers into green when connected to the server
    if (key.text === 'z') {
        Entities.editEntity(numtext1, {textColor: {red:0, green:255, blue:0}});
        //Entities.editEntity(numtext2, {textColor: {red:0, green:255, blue:0}});
    }
    // if (key.text === 'z') {
    //     connectedVisible = true;
    //     Entities.editEntity(connected, {visible: connectedVisible});
    //     print("connected visibility");
    // }
});

Controller.keyPressEvent.connect(function(key) {
    print("you pressed " + key.text);

    // make the countdown cnumbers into black again when disconnected to the server
    if (key.text === 'x') {
        Entities.editEntity(numtext1, {textColor: {red:255, green:255, blue:255}});
        //Entities.editEntity(numtext2, {textColor: {red:255, green:255, blue:255}});
    }
    // if (key.text === 'x') {
    //     connectedVisible = false;
    //     Entities.editEntity(connected, {visible: connectedVisible});
    //     print("connected visibility");
    // }
});

// change color to blue 
var isBlue = false;
Controller.keyPressEvent.connect(function(key) {
    print("you pressed " + key.text);

    if (key.text === 'q') {
        if (!isBlue) {
            Entities.editEntity(numtext1, {textColor: {red:0, green:0, blue: 255}});
            isBlue = true;
        } else {
            // change back to green
            Entities.editEntity(numtext1, {textColor: {red:0, green:255, blue: 0}});
            isBlue = false;
        }
    }
});

// Create a new mapping object
var mapping = Controller.newMapping("zero");

// Add a route to the mapping object
// fix lefthand controller
mapping.from(Controller.Standard.LeftHand).to(function (value) {
    return Vec3.ZERO;
});

// fix righthand controller
mapping.from(Controller.Standard.RightHand).to(function (value) {
    return Vec3.ZERO;
});


// Enable/disable hand movement via controller
// 'f'
var controllerFixed = false;
Controller.keyPressEvent.connect(function(key) {
    if (key.text === 'f') {
        if (controllerFixed === false) {
            controllerFixed = true;
            print("controller fix enabled.");
            Controller.enableMapping("zero");
        } else {
            controllerFixed = false;
            print("controller fix disabled.");
            Controller.disableMapping("zero");
        }
    }
});
