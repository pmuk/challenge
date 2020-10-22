use std::fs::File;
use std::io::Read;
use std::io::Write;

struct Event {
    elems: std::vec::Vec<(String, String)>
}

trait ToJson {
    fn to_json(self) -> String;
}

impl ToJson for Event{
    fn to_json(self)->String{
        return format!("{}{}{}","{",
            self.elems.iter().skip(1)
            .fold(format!("{}:{}",self.elems[0].0, self.elems[0].1), |acc,x|format!("{},\"{}\": \"{}\"",acc, x.0, x.1))
            ,"}"
        );
    }
}

fn create_event(str:String)->Event{
    let mut els = Vec::new();
    let tmp:Vec<&str>= str.split("\" ").collect();
    for s in &tmp{
        let splitted:Vec<_>= s.split(": \"").collect();
        els.push((splitted[0].trim().to_string(),splitted[1].trim().to_string()));
    }

    return Event{elems:els};
}

fn main() {
    let mut file = File::open(".\\src\\event_data.txt").unwrap();
    let mut contents = String::new();
    file.read_to_string(&mut contents).unwrap();
    println!("{}",contents);

    let e = create_event("time: \"12:34:56\" challenge: \"Find the fifth value in the \\\"sequence\\\"\" hint: \"WE9SIHdpdGggMHgxN0YK\" one: \"0x154\" two: \"0x150\" three: \"0x14A\" four: \"0x144\"".to_string());

    let json = e.to_json();

    let mut file_writer = std::fs::File::create("part_A_rust.txt").expect("create failed");
    file_writer.write_all(json.as_bytes()).expect("write failed");
    println!("data written to file" );
}
