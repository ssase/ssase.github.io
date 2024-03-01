---
layout: post
title: "Set Up Your Blog At Github.io"
date: 2024-01-15 08:30:28 +0800
published: true
categories: [Tutorial, Blog]
tags: [ruby, jekyll, gitHub pages]
# The categories of each post are designed to contain up to two elements, and the number of elements in tags can be zero to infinity. 
# TAG names should always be lowercase
author: max
toc: true
comments: false
math: false
mermaid: false
# Mermaid is a great diagram generation tool
---

There have been a lot of instructions about how to set up a blog at github.io, but it still cost me 3 nights to finish. So I believe that recording what I had done when built this blog may help others who meet the same issues.

## Run Your Blog Locally

Whether for testing or to see what you've changed faster, it is recommended to run your blog locally, below is how to set up it.

### Install Dependencies for Jekyll

My system is Ubuntu-22.04.3, if yours is mac, windows or other linux, here is the place for you to get more information [Jekyll Docs: installation](https://jekyllrb.com/docs/installation/).

#### 1. Install Ruby:

```shell
sudo apt update
sudo apt-get install ruby-full build-essential zlib1g-dev
```

> Avoid installing RubyGems packages (called gems) as the root user. Instead, set up a gem installation directory for your user account. 
{: .prompt-tip }

It is a good suggestion, though I did not follow.

#### 2. Add environment variables to configure the gem installation path

Add variables below to `.zshrc` if you use `zsh` or `.bashrc` if you use `bash`.
```shell
# Install Ruby Gems to ~/gems
export GEM_HOME="$HOME/gems"
export PATH="$HOME/gems/bin:$PATH"
```

#### 3. Install Jekyll and Bundler
```shell
gem install jekyll bundler
```

#### 4. Change sources if installation is slow
- For gem
```shell
gem sources --add https://mirrors.tuna.tsinghua.edu.cn/rubygems/ --remove https://rubygems.org/
```
- For bundler
```shell
bundle config mirror.https://rubygems.org https://mirrors.tuna.tsinghua.edu.cn/rubygems
```

#### 5. Trouble shooting

- Bundler::PermissionError

I met the error below when excuse `gem install jekyll bundler`:
```shell
Bundler::PermissionError: There was an error while trying to write to `/xxx/cache/xxx.gem`. It is likely that you need to grant write permissions for that path.  
```
Using `gem install jekyll bundler --user-install` instead helped for me.

- zsh: command not found: jekyll

When I wanted to use `jekyll` command, I ran into this error `zsh: command not found: jekyll`.
I fixed it by adding this line to `.zshrc`.
```shell
export PATH=$PATH:/home/YOUR_USER_NAME/.local/share/gem/ruby/3.0.0/bin
```

### Choose a Jekyll Theme

You can pick up a theme from here [Jekyll Theme](https://jekyllrb.com/docs/themes/).

Or just generate a default theme using `jekyll new YOUR_BLOG_NAME`

Visit [Jekyll Doc](https://jekyllrb.com/docs/) for more information.

## Set Up Your Blog at Github.io

I choose Chirpy as my theme, if you are the same, you can visit [Getting start with Chirpy](https://chirpy.cotes.page/posts/getting-started/) for more information.

Or if you do not, you can follow other theme's instruction or just visit <https://pages.github.com/>.

#### Add a Rakefile to generate a new post conveniently

After you clone your repository to local, new a file `Rakefile`, and add contens below. Then you can use command `rake newpost` at shell to add a new post conveniently.

```ruby
require "stringex"

posts_dir       = "_posts"
new_post_ext    = "md"

task :newpost, :title do |t, args|
  if args.title
    title = args.title
  else
    title = get_stdin("Enter a title for your post: ")
  end

  mkdir_p "#{posts_dir}"
  filename = "#{posts_dir}/#{Time.now.strftime('%Y-%m-%d')}-#{title.to_url}.#{new_post_ext}"
  if File.exist?(filename)
    abort("rake aborted!") if ask("#{filename} already exists. Do you want to overwrite?", ['y', 'n']) == 'n'
  end
  puts "Creating new post: #{filename}"
  open(filename, 'w') do |post|
    post.puts "---"
    post.puts "layout: post"
    post.puts "title: \"#{title.gsub(/&/,'&amp;')}\""
    post.puts "date: #{Time.now.strftime('%Y-%m-%d %H:%M:%S')} +0800"
    post.puts "published: true"
    post.puts "categories: [Animal, Insect]"
    post.puts "tags: [bee]"
    post.puts "# The categories of each post are designed to contain up to two elements, and the number of elements in tags can be zero to infinity. "
    post.puts "# TAG names should always be lowercase"
    post.puts "toc: false"
    post.puts "comments: false"
    post.puts "math: false"
    post.puts "mermaid: false"
    post.puts "# Mermaid is a great diagram generation tool"
    post.puts "---"
  end
end

def get_stdin(message)
  print message
  STDIN.gets.chomp
end

def ask(message, valid_options)
  if valid_options
    answer = get_stdin("#{message} #{valid_options.to_s.gsub(/"/, '').gsub(/, /,'/')} ") while !valid_options.include?(answer)
  else
    answer = get_stdin(message)
  end
  answer
end
```

> You might need to excuse `gem install stringex` first before using `Rakefile`.
{: .prompt-tip }

Have a nice day!