
#---------------------------------
# Build and configure PLATFORM
#---------------------------------

#prepare_rhel6_for_puppet ${EXTRA_PKGS}

#---------------------------------------
# Install RoR and necessry dependencies
#---------------------------------------

# Install Rails without documentation for saving time
gem install rails -v 3.2.13 --no-rdoc --no-ri 

if [ $? -ne 0 ]
then
  	exit
fi

# Start mysqld
service mysqld start

#----------------------------
# Create a demo RoR web site
#----------------------------

ROR_APP_DIR=/home/ec2-user/rails_projects
ROR_APP_NAME=hello

#
# Create a functioning Rails application skeleton
#
export HOME=/home/ec2-user

mkdir ${ROR_APP_DIR}

# Set up current working directory
cd ${ROR_APP_DIR}

# Create a skeleton with MySQL supported
#which rails >> /var/log/ror.log 2>&1

rails new $ROR_APP_NAME -d mysql 

# Install a necessary gem
gem install execjs --no-rdoc --no-ri

# Set up current working directory
cd ${ROR_APP_DIR}/${ROR_APP_NAME}

# Modify Gemfile and rebuild it
cat << 'EOHD' >> Gemfile
gem 'execjs'
gem 'therubyracer'
EOHD

# Install dependencies specified in Gemfile
bundle install

# Create the Rails app database
mysqladmin create ${ROR_APP_NAME}_development

#
# Create a controller called entries associated with sign_in view
#
rails generate controller entries sign_in

# Modify app/controllers/entries_controller.rb
cat << 'EOHD' > app/controllers/entries_controller.rb
class EntriesController < ApplicationController
  def sign_in
    @name = params[:visitor_name]

    unless @name.blank?
      @entry = Entry.create({:name => @name})
    end

    @entries = Entry.all
  end
end
EOHD

# Modify app/views/entries/sign_in.html.erb
cat << 'EOHD' > app/views/entries/sign_in.html.erb
<h1>Ruby on Rails Demo Application: Guestbook </h1>
<p></p>
<h2>Hello <%= @name %></h2>

<%= form_tag :action => 'sign_in' do %>
   <p>Enter your name:
   <%= text_field_tag 'visitor_name', @name %></p>

   <%= submit_tag 'Sign in' %>
<% end %>
<p>Previous visitors:</p>
<ul>
<% @entries.each do |entry| %>
  <li><%= entry.name %></li>
<% end %>
</ul>
EOHD

# Modify config/routes.rb
# Make the new default page
cat << 'EOHD' > config/routes.rb
Hello::Application.routes.draw do
  get "entries/sign_in"
  root :to => "entries#sign_in"
  match ':controller(/:action(/:id(.:format)))'
end
EOHD

# Remove the original default page
mv public/index.html index2.html

#
# Create a model called entry
#
rails generate model entry

# Modify db/migrate/*.rb
cat << 'EOHD' > db/migrate/$(ls db/migrate)
class CreateEntries < ActiveRecord::Migration
  def change
    create_table :entries do |t|
      t.string :name
      t.timestamps
    end
  end
end
EOHD

# Run db migrate
rake db:migrate

# Modify app/models/entry.rb
cat << 'EOHD' > app/models/entry.rb
class Entry < ActiveRecord::Base
  attr_accessible :name
end
EOHD

#
# Start the default RoR web server WEBRICK
#
rails server -p 80 
