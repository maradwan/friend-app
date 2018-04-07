require 'spec_helper'

#Packages

describe package('ec2-ami-tools'), :if => os[:family] == 'ubuntu' do
  it { should be_installed }
end

describe package('python-pip'), :if => os[:family] == 'ubuntu' do
  it { should be_installed }
end

describe package('libpipeline1:amd64'), :if => os[:family] == 'ubuntu' do
  it { should be_installed }
end

describe package('nginx-common'), :if => os[:family] == 'ubuntu' do
  it { should be_installed }
end

describe package('nginx-extras'), :if => os[:family] == 'ubuntu' do
  it { should be_installed }
end

describe package('python-pymysql'), :if => os[:family] == 'ubuntu' do
  it { should be_installed }
end

# Port Open
describe port(80) do
  it { should be_listening }
end
