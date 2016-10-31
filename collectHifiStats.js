// Last updated 10/31/16 by Ha




var ENDPOINT_URL = "https://qcy5nql2a4.execute-api.us-west-2.amazonaws.com/prod"; // NEW URL!


/*---------------------------------*/
var user_id = 920610; // SONA ID
var condition = "A"; // condition type
    // A - whole body with free arm
    // B - whole body with fixed arm
    // C - just face and hands
/*---------------------------------*/




var COLLECT_EVERY = 100; // 100 milliseconds
//var COLLECT_EVERY = 1000;
var SEND_EVERY = 10; // 10 batches = 1 second

var batch = [];
var run = false;


var connectSound = SoundCache.getSound("file:///" + Paths.resources + "sounds/hello.wav");
var disconnectSound = SoundCache.getSound("file:///" + Paths.resources + "sounds/goodbye.wav");
var connect = Audio.playSound(connectSound, {localOnly: true});
var disconnect = Audio.playSound(disconnectSound, {localOnly: true});


Controller.keyPressEvent.connect(function(key) {
    if (key.text === 'z') {
        print("start sending data...");
        run = true;
        //var connect = Audio.playSound(connectSound, {localOnly: true});
        // injector
    }
    if (key.text === 'x') {
        print("stop sending data");
        run = false;
        //var disconnect = Audio.playSound(disconnectSound, {localOnly: true});
    }
});

Script.setInterval(function () {
    if (run) {
        Stats.forceUpdateStats();
        batch.push(getStats());
        //print("before: " + JSON.stringify(batch));
        if (batch.length >= SEND_EVERY) {
            var req = new XMLHttpRequest();
            req.open("POST", ENDPOINT_URL, false); // post to DynamoDB
            req.send(JSON.stringify(batch));
            print(JSON.stringify(batch));
            batch = []; // refresh the batch
            print("collecting data...");
        }
    }
}, COLLECT_EVERY);

function getStats() {
    return {
        "time": Date.now() / 1000.0,
        user_id: user_id,
        condition: condition,
        framerate: Stats.framerate,
        avatar_ping: Stats.avatarPing,
        tracked_head_position_x: MyAvatar.getTrackedHeadPosition().x,
        tracked_head_position_y: MyAvatar.getTrackedHeadPosition().y,
        tracked_head_position_z: MyAvatar.getTrackedHeadPosition().z,
        joint_head_position_x: MyAvatar.getJointPosition('HeadTop_End').x,
        joint_head_position_y: MyAvatar.getJointPosition('HeadTop_End').y,
        joint_head_position_z: MyAvatar.getJointPosition('HeadTop_End').z,
        joint_head_rotation_x: MyAvatar.getJointRotation('HeadTop_End').x,
        joint_head_rotation_y: MyAvatar.getJointRotation('HeadTop_End').y,
        joint_head_rotation_z: MyAvatar.getJointRotation('HeadTop_End').z,
        joint_head_rotation_w: MyAvatar.getJointRotation('HeadTop_End').w,
        camera_orientation_x: Camera.orientation.x,
        camera_orientation_y: Camera.orientation.y,
        camera_orientation_z: Camera.orientation.z,
        camera_orientation_w: Camera.orientation.w,
        camera_position_x: Camera.getPosition().x,
        camera_position_y: Camera.getPosition().y,
        camera_position_z: Camera.getPosition().z,
        avatar_position_x: MyAvatar.position.x,
        avatar_position_y: MyAvatar.position.y,
        avatar_position_z: MyAvatar.position.z,
        left_hand_position_x: MyAvatar.getJointPosition('LeftHand').x,
        left_hand_position_y: MyAvatar.getJointPosition('LeftHand').y,
        left_hand_position_z: MyAvatar.getJointPosition('LeftHand').z,
        left_hand_rotation_x: MyAvatar.getJointRotation('LeftHand').x,
        left_hand_rotation_y: MyAvatar.getJointRotation('LeftHand').y,
        left_hand_rotation_z: MyAvatar.getJointRotation('LeftHand').z,
        left_hand_rotation_w: MyAvatar.getJointRotation('LeftHand').w,
        right_hand_position_x: MyAvatar.getJointPosition('RightHand').x,
        right_hand_position_y: MyAvatar.getJointPosition('RightHand').y,
        right_hand_position_z: MyAvatar.getJointPosition('RightHand').z,
        right_hand_rotation_x: MyAvatar.getJointRotation('RightHand').x,
        right_hand_rotation_y: MyAvatar.getJointRotation('RightHand').y,
        right_hand_rotation_z: MyAvatar.getJointRotation('RightHand').z,
        right_hand_rotation_w: MyAvatar.getJointRotation('RightHand').w,
        right_controller_position_x: Controller.getPoseValue(Controller.Standard.RightHand).translation.x,
        right_controller_position_y: Controller.getPoseValue(Controller.Standard.RightHand).translation.y,
        right_controller_position_z: Controller.getPoseValue(Controller.Standard.RightHand).translation.z,
        right_controller_rotation_x: Controller.getPoseValue(Controller.Standard.RightHand).rotation.x,
        right_controller_rotation_y: Controller.getPoseValue(Controller.Standard.RightHand).rotation.y,
        right_controller_rotation_z: Controller.getPoseValue(Controller.Standard.RightHand).rotation.z,
        right_controller_rotation_w: Controller.getPoseValue(Controller.Standard.RightHand).rotation.w,
        left_controller_position_x: Controller.getPoseValue(Controller.Standard.LeftHand).translation.x,
        left_controller_position_y: Controller.getPoseValue(Controller.Standard.LeftHand).translation.y,
        left_controller_position_z: Controller.getPoseValue(Controller.Standard.LeftHand).translation.z,
        left_controller_rotation_x: Controller.getPoseValue(Controller.Standard.LeftHand).rotation.x,
        left_controller_rotation_y: Controller.getPoseValue(Controller.Standard.LeftHand).rotation.y,
        left_controller_rotation_z: Controller.getPoseValue(Controller.Standard.LeftHand).rotation.z,
        left_controller_rotation_w: Controller.getPoseValue(Controller.Standard.LeftHand).rotation.w
    };
}
