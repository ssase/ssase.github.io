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
    post.puts "author: min"
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