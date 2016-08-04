// master_script.js
// last updated 8/4/16 by HA
// for HiFi Study


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






// make wall disappear when b is pressed
var original_wall = '5af10887-444c-4283-928d-059644ca36e8';
var visible = Entities.getEntityProperties(original_wall, visible);
//var wall = '17cdd587-875b-4d79-96c1-5a055683e0ef';
//var visible = Entities.getEntityProperties(wall, visible);

Controller.keyPressEvent.connect(function(key) {
    print("you pressed " + key.text);
    if (key.text == 'b') {
        visible = !visible;
        //Entities.editEntity(wall, {visible: visible});
        Entities.editEntity(original_wall, {visible: visible});
    }
});


// make the texts change from 20 to 0 using c key
var original_numtext1 = 'bd153e01-3247-433a-b06d-023f2c435851';
var original_numtext2 = 'ca72b2d1-f0ce-47b8-9a49-1525bc076a55';

//var numtext1 = 'bb2d033d-977c-4e8e-b308-e2b7e1e2247f';
//var numtext2 = 'c4f24e58-36b6-4267-8011-0f69970e4d7c';
var num = 20;
//Entities.editEntity(numtext1, {text: num});
//Entities.editEntity(numtext2, {text: num});

Entities.editEntity(original_numtext1, {text: num});
Entities.editEntity(original_numtext2, {text: num});


// FIXME two computers track diffrent num
Controller.keyPressEvent.connect(function(key) {
    if (key.text == 'c') {
        if (num > 0) {
            num--;
        } else {
            num = 20;
        }
        //Entities.editEntity(numtext1, {text: num});
        //Entities.editEntity(numtext2, {text: num});

        Entities.editEntity(original_numtext1, {text: num});
        Entities.editEntity(original_numtext2, {text: num});
    }
});


// numtext1, numtext2 visibility
// disable visibility for numtext1 and numtext2
//var visible_counter = Entities.getEntityProperties(numtext1, visible);
var visible_counter = Entities.getEntityProperties(original_numtext1, visible);

Controller.keyPressEvent.connect(function(key) {
    if (key.text == 'm') {
        visible_counter = !visible_counter;
        //Entities.editEntity(numtext1, {visible: visible_counter});
        //Entities.editEntity(numtext2, {visible: visible_counter});

        Entities.editEntity(original_numtext1, {visible: visible_counter});
        Entities.editEntity(original_numtext2, {visible: visible_counter});
    }
});


// TODO not so sure what this does
// timout with v key
Controller.keyPressEvent.connect(function(key) {
    if (key.text == 'v') {
        visible = !visible;
        if (!visible) {
            //Entities.editEntity(wall, {visible: visible});
            Entities.editEntity(original_wall, {visible: visible});
        } else {
            Script.setTimeout(function () {
                //Entities.editEntity(wall, {visible: visible});
                Entities.editEntity(original_wall, {visible: visible});
            }, 300000);
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


// Use 'z' key to enable/disable hand movement via controller
var controllerFixed = false;
Controller.keyPressEvent.connect(function(key) {
    if (key.text == 'z') {
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
