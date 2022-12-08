use std::{
    collections::{HashMap, HashSet},
    fs::File,
    io::{self, BufRead, BufReader},
};

type FSID = u64;

#[derive(Debug, Clone)]
struct AOCFile {
    name: String,
    size: u64,
    parent: FSID,
}

#[derive(Debug, Clone)]
struct AOCDirectory {
    name: String,
    elements: HashSet<FSID>,
    parent: Option<FSID>,
}

#[derive(Debug, Clone)]
enum FSElement {
    Directory(AOCDirectory),
    File(AOCFile),
}

struct FileSystem {
    elements: HashMap<FSID, FSElement>,
}

impl FileSystem {
    pub fn new() -> FileSystem {
        let root = AOCDirectory {
            name: String::from("/"),
            elements: HashSet::new(),
            parent: None,
        };

        FileSystem {
            elements: HashMap::from([(0, FSElement::Directory(root))]),
        }
    }

    pub fn create(&mut self, element: FSElement) -> FSID {
        let id = self.elements.len() as FSID;

        match element.clone() {
            FSElement::Directory(d) => {
                self.elements.insert(id, element);

                if let Some(FSElement::Directory(parent)) =
                    self.elements.get_mut(&d.parent.unwrap())
                {
                    parent.elements.insert(id);
                }
            }
            FSElement::File(f) => {
                self.elements.insert(id, element);

                if let Some(FSElement::Directory(parent)) = self.elements.get_mut(&f.parent) {
                    parent.elements.insert(id);
                }
            }
        };

        return id;
    }

    pub fn get(&self, id: FSID) -> &FSElement {
        self.elements.get(&id).unwrap()
    }

    pub fn get_parent_id(&self, element_id: FSID) -> FSID {
        match self.get(element_id) {
            FSElement::Directory(d) => d.parent.unwrap_or(0),
            FSElement::File(f) => f.parent,
        }
    }

    pub fn get_size(&self, element_id: FSID) -> u64 {
        match self.get(element_id) {
            FSElement::Directory(d) => d.elements.iter().map(|id| self.get_size(*id)).sum(),
            FSElement::File(f) => f.size,
        }
    }

    pub fn is_directory(&self, fsid: FSID) -> bool {
        match self.get(fsid) {
            FSElement::Directory(_) => true,
            _ => false,
        }
    }

    pub fn get_directory(&self, fsid: FSID) -> &AOCDirectory {
        match self.get(fsid) {
            FSElement::Directory(d) => d,
            other => panic!("Not a directory: {other:?}"),
        }
    }

    pub fn get_all_directories(&self) -> Vec<(FSID, &AOCDirectory)> {
        self.elements.keys()
            .filter(|id| self.is_directory(**id))
            .map(|id| (*id, self.get_directory(*id)))
            .collect()
    }

    pub fn get_subdirectories(&self, parent: FSID) -> Vec<(FSID, &AOCDirectory)> {
        self.get_directory(parent)
            .elements
            .iter()
            .filter(|id| self.is_directory(**id))
            .map(|id| (*id, self.get_directory(*id)))
            .collect()
    }

    pub fn get_name(&self, fsid: FSID) -> &str {
        match self.get(fsid) {
            FSElement::Directory(d) => &d.name,
            FSElement::File(f) => &f.name,
        }
    }

    pub fn has_subdirectory(&self, parent_id: FSID, subdir_name: &str) -> bool {
        for (_, subdir) in self.get_subdirectories(parent_id) {
            if subdir.name == subdir_name {
                return true;
            }
        }

        false
    }

    pub fn get_subdirectory(
        &self,
        parent_id: FSID,
        subdir_name: &str,
    ) -> Option<(FSID, &AOCDirectory)> {
        for (id, subdir) in self.get_subdirectories(parent_id) {
            if subdir.name == subdir_name {
                return Some((id, subdir));
            }
        }

        None
    }
}

fn print_directory(file_system: &FileSystem, dir_id: FSID, indent: usize) {
    let dir = file_system.get_directory(dir_id);
    println!("{:indent$}- {} (dir)", "", dir.name, indent = indent);

    for id in dir.elements.iter() {
        match file_system.get(*id) {
            FSElement::Directory(_) => print_directory(file_system, *id, indent + 4),
            FSElement::File(f) => println!(
                "{:indent$}- {} (file, size={})",
                "",
                f.name,
                f.size,
                indent = indent + 4
            ),
        }
    }
}

fn main() -> io::Result<()> {
    let file = File::open("input.txt")?;
    let lines = BufReader::new(file).lines().map(|l| l.unwrap());
    let mut file_system: FileSystem = FileSystem::new();
    let mut current_dir_id = 0 as FSID;

    for line in lines.skip(1) {
        //println!("{line}");

        let parts = line.split_whitespace().collect::<Vec<_>>();

        match &parts[..] {
            ["$", "cd", ".."] => {
                current_dir_id = file_system.get_parent_id(current_dir_id);
            }
            ["$", "cd", dir_name] => {
                let dir_name = String::from(*dir_name);

                current_dir_id = if file_system.has_subdirectory(current_dir_id, &dir_name) {
                    file_system
                        .get_subdirectory(current_dir_id, &dir_name)
                        .unwrap()
                        .0
                } else {
                    file_system.create(FSElement::Directory(AOCDirectory {
                        name: dir_name,
                        elements: HashSet::new(),
                        parent: Some(current_dir_id),
                    }))
                };
            }
            ["$", "ls"] => continue,
            ["dir", dir] => {
                file_system.create(FSElement::Directory(AOCDirectory {
                    name: String::from(*dir),
                    elements: HashSet::new(),
                    parent: Some(current_dir_id),
                }));
            }
            [file_size, file_name] => {
                file_system.create(FSElement::File(AOCFile {
                    name: String::from(*file_name),
                    size: file_size.parse().unwrap(),
                    parent: current_dir_id,
                }));
            }
            parts => panic!("Unable to parse {parts:?}"),
        }
    }

    print_directory(&file_system, 0, 0);
    let sum: u64 = file_system
        .get_all_directories()
        .iter()
        .map(|(id, _)| file_system.get_size(*id))
        .filter(|size| size <= &100000)
        .sum();
    println!("{sum}");
    Ok(())
}
