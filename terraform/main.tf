provider "aws" {
  region = "eu-west-1"
}

resource "aws_launch_configuration" "friend" {
    image_id = "${var.image_id}"
    instance_type = "t2.nano"
    security_groups = ["${aws_security_group.instance.id}"]
    key_name = "maradwan-keys"
    user_data = <<-EOF
              #!/bin/bash
              salt-call --local state.highstate
              sudo python /home/ubuntu/friend/app/runserver.py &
              EOF

lifecycle {
  create_before_destroy = true
 }
}


variable "server_port" {
   description = "The port the server will use for http requests"
   default = 80
}


resource "aws_security_group" "instance" {
   name  = "terraform-instance"

  ingress {

   from_port = "${var.server_port}"
   to_port   = "${var.server_port}"
   protocol = "tcp"
   cidr_blocks = ["0.0.0.0/0"]
 }

 egress {
  from_port = 0
  to_port = 0
  protocol = "-1"
  cidr_blocks = ["0.0.0.0/0"]
}

 lifecycle {
  create_before_destroy = true

 }
}


data "aws_availability_zones" "all" {}

resource "aws_autoscaling_group" "friend" {
  name                 = "${var.asg_name}-${aws_launch_configuration.friend.name}"
  launch_configuration = "${aws_launch_configuration.friend.id}"
  availability_zones = ["${data.aws_availability_zones.all.names}"]

  load_balancers = ["${aws_elb.friend.name}"]
  health_check_type = "ELB"
  min_elb_capacity          = "3"
  termination_policies      = ["OldestLaunchConfiguration"]
  desired_capacity          = "${var.desired_capacity}"


  max_size                  = "${var.max_size}"
  min_size                  = "${var.min_size}"


tag {
  key = "Name"
  value = "Friend-app"
  propagate_at_launch = true
 }

lifecycle {
  create_before_destroy = true
 }
}

resource "aws_security_group" "elb" {
  name = "terraform-elb-1"
  
  ingress { 

   from_port = 80
   to_port = 80
   protocol = "tcp"
   cidr_blocks = ["0.0.0.0/0"]
 }

  egress { 
  from_port = 0
  to_port = 0
  protocol = "-1"
  cidr_blocks = ["0.0.0.0/0"]
 }
}


resource "aws_elb" "friend" { 

  name = "friend"
  availability_zones = ["${data.aws_availability_zones.all.names}"]
  security_groups = ["${aws_security_group.elb.id}"] 
 
  listener { 
   
   lb_port 	= 80
   lb_protocol	= "http"
   instance_port = "${var.server_port}"
   instance_protocol = "http"

 }

 health_check { 
  healthy_threshold = 2
  unhealthy_threshold = 2
  timeout   = 3
  interval  = 300
  target  = "HTTP:${var.server_port}/"
 }
}

resource "aws_autoscaling_policy" "app-scale-out" {
  name = "app-scale-out"
  scaling_adjustment = 3
  adjustment_type = "ChangeInCapacity"
  cooldown = 300
  autoscaling_group_name = "${aws_autoscaling_group.friend.name}"
}

resource "aws_autoscaling_policy" "app-scale-in" {
  name = "app-scale-in"
  scaling_adjustment = -1
  adjustment_type = "ChangeInCapacity"
  cooldown = 300
  autoscaling_group_name = "${aws_autoscaling_group.friend.name}"
}

resource "aws_cloudwatch_metric_alarm" "app-cpu-up" {
  alarm_name          = "app-cpu-up"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  threshold           = "4"
  metric_name         = "CPUUtilization"
  namespace           = "AWS/EC2"
  period              = "60"
  evaluation_periods  = "3"
  statistic           = "Average"

  dimensions {
    AutoScalingGroupName = "${aws_autoscaling_group.friend.name}"
  }

  alarm_description = "This metric monitors app cpu utilization"
  alarm_actions     = [ "${aws_autoscaling_policy.app-scale-out.arn}" ]
}

resource "aws_cloudwatch_metric_alarm" "app-cpu-down" {
  alarm_name          = "app-cpu-down"
  comparison_operator = "LessThanOrEqualToThreshold"
  threshold           = "1"
  metric_name         = "CPUUtilization"
  namespace           = "AWS/EC2"
  period              = "60"
  evaluation_periods  = "3"
  statistic           = "Average"

  dimensions {
    AutoScalingGroupName = "${aws_autoscaling_group.friend.name}"
  }

  alarm_description = "This metric monitors app cpu utilization"
  alarm_actions     = [ "${aws_autoscaling_policy.app-scale-in.arn}" ]
}
