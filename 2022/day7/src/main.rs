use std::{
    fs::File,
    io::{self, BufRead, BufReader}, collections::HashMap,
};

#[derive(Debug)]
struct AOCFile {
    name: String,
    size: u64,
}

#[derive(Debug)]
struct AOCDirectory {
    name: String,
    elements: HashMap<String, Box<FSElement>>,
    parent: Option<Box<AOCDirectory>>,
}

#[derive(Debug)]
enum FSElement {
    Directory(AOCDirectory),
    File(AOCFile),
}

fn print_directory(dir: &AOCDirectory, indent: usize) {
    println!("{:indent$}- {} (dir)", "", dir.name, indent=indent);

    for element in dir.elements.values() {
        match element.as_ref() {
            FSElement::Directory(d) => print_directory(d, indent + 4),
            FSElement::File(f) =>     println!("{:indent$}- {} (file, size={})", "", f.name, f.size, indent=indent),
            e => panic!("Not handled: {e:?}")
        }
    }
}

fn main() -> io::Result<()> {
    let file = File::open("input.txt")?;
    let lines = BufReader::new(file).lines().map(|l| l.unwrap());
    let mut root = Box::new(AOCDirectory {
        name: String::from("/"),
        elements: HashMap::new(),
        parent: None,
    });
    let mut current_dir = root.as_mut();

    for line in lines {
        let parts = line.split_whitespace().collect::<Vec<_>>();
        match &parts[..] {
            ["$", "cd", dir_name] => {
                let dir_name = String::from(*dir_name);

                if dir_name != current_dir.name {
                    if current_dir.elements.contains_key(&dir_name) {
                        current_dir = match current_dir.elements.get_mut(&dir_name).unwrap().as_mut(){
                          FSElement::Directory(d) => d,
                          element => panic!("{element:?} is not a directory")  
                        };
                    }
                    else {
                        current_dir.elements.insert(dir_name.clone(), Box::new(FSElement::Directory(AOCDirectory {
                            name: dir_name,
                            elements: HashMap::new(),
                            parent: Some(Box::new(*current_dir))
                        })));
                    }
                }
            }
            ["$", "ls"] => println!("List directory"),
            ["dir", dir] => println!("Directory {dir}"),
            [file_size, file_name] => println!("File {file_name} with size {file_size}"),
            parts => panic!("Unable to parse {parts:?}"),
        }
    }

    print_directory(&root, 0);
    Ok(())
}
